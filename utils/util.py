import numpy as np
import pandas as pd
import math
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from RankingFacts.nutrition_label_utility import *
from scipy.stats import norm


def fair_metrics(dataset, pred):
  dataset_pred = dataset.copy()
  dataset_pred.labels = pred
  
  cols = ['statistical_parity_difference', 'equal_opportunity_difference', 'average_abs_odds_difference',  'disparate_impact', 'theil_index']
  obj_fairness = [[0,0,0,1,0]]
  
  fair_metrics = pd.DataFrame(data=obj_fairness, index=['objective'], columns=cols)
  
  for attr in dataset_pred.protected_attribute_names:
      idx = dataset_pred.protected_attribute_names.index(attr)
      privileged_groups =  [{attr:dataset_pred.privileged_protected_attributes[idx][0]}] 
      unprivileged_groups = [{attr:dataset_pred.unprivileged_protected_attributes[idx][0]}] 
      
      classified_metric = ClassificationMetric(dataset, 
                                                    dataset_pred,
                                                    unprivileged_groups=unprivileged_groups,
                                                    privileged_groups=privileged_groups)

      metric_pred = BinaryLabelDatasetMetric(dataset_pred,
                                                    unprivileged_groups=unprivileged_groups,
                                                    privileged_groups=privileged_groups)

      row = pd.DataFrame([[ 
                            metric_pred.mean_difference(),
                            classified_metric.equal_opportunity_difference(),
                            classified_metric.average_abs_odds_difference(),
                            metric_pred.disparate_impact(),
                            classified_metric.theil_index()]],
                          columns  = cols,
                          index = [attr]
                        )
      fair_metrics = pd.concat([fair_metrics, row])
  
  fair_metrics = fair_metrics.replace([-np.inf, np.inf], 2)
      
  return fair_metrics


def compute_p_FAIR(_data, _att, _protected_group, _y_col="Score", top_k = 100, round_default = 2):
    """
    Compute p-value using FA*IR algorithm

    Attributes:
        _data: dataframe that stored the data
        _att: sensitive attribute name
        _protected_group: the value of sensitive attribute for protected group
        _y_col: the column that stores the values of ranking
        top_k: the top ranking to verify group fairness
        round_default: threshold of round function
    Return:  rounded p-value and adjusted significance level in FA*IR
    """
    _data.sort_values(by=_y_col, ascending=False, inplace=True)
    _data.reset_index(drop=True, inplace=True)
    if len(_data)/2 < top_k:
        top_k = int(len(_data)/2)
    pos_protected = _data[_data[_att]==_protected_group].index+1
    pro_prob = len(pos_protected)/len(_data)

    # transform ranking to a ranking of tuples with (id,"pro")/(id,"unpro") to run FA*IR
    transformed_ranking = []
    for index, row in _data.head(top_k).iterrows():
        if row[_att] == _protected_group:
            transformed_ranking.append([index,"pro"])
        else:
            transformed_ranking.append([index,"unpro"])

    p_value, isFair, posiFail, alpha_c, pro_needed_list = computeFairRankingProbability(top_k, pro_prob, transformed_ranking)
    return p_value, isFair, posiFail, round(alpha_c,round_default)

def compute_p_pairs(_data, _att, _protected_group, _y_col="Score", run_time = 100, round_default = 2):
    """
    Compute p-value using Pairwise oracle

    Attributes:
        _data: dataframe that stored the data
        _att: sensitive attribute name
        _protected_group: the value of sensitive attribute for protected group
        _y_col: the column that stores the values of ranking
        run_time: simulation times for pairwise comparison
        round_default: threshold of round function
    Return:  rounded p-value
    """
    _data.sort_values(by=_y_col, ascending=False, inplace=True)
    _data.reset_index(drop=True, inplace=True)
    pos_protected = _data[_data[_att]==_protected_group].index+1
    pro_prob = len(pos_protected)/len(_data)
    total_n = len(_data)
    pro_n = len(pos_protected)
    seed_random_ranking = [x for x in range(total_n)]  # list of IDs
    seed_f_index = [x for x in range(pro_n)]  # list of IDs
    
    sim_df = pd.DataFrame(columns=["Run", "pair_n"])
    # run the simulation of ranking generation, in each simulation, generate a fair ranking with input N and size of sensitive group
    for ri in range(run_time):
        output_ranking = mergeUnfairRanking(seed_random_ranking, seed_f_index, pro_prob)
        position_pro_list = [i for i in range(total_n) if output_ranking[i] in seed_f_index]
        count_sensi_prefered_pairs = 0
        for i in range(len(position_pro_list)):
            cur_position = position_pro_list[i]
            left_sensi = pro_n - (i + 1)
            count_sensi_prefered_pairs = count_sensi_prefered_pairs + (total_n - cur_position - left_sensi)
        cur_row = [ri + 1, count_sensi_prefered_pairs]
        sim_df.loc[sim_df.shape[0]] = cur_row

    input_pair_n, _, _ = computePairN(_att, _protected_group, _data)
    pair_samples = list(sim_df["pair_n"].dropna())
    return round(Cdf(pair_samples, input_pair_n), round_default)

def compute_p_proportion(_data, _att, _protected_group, _y_col="Score", top_k = 100, round_default = 2):
    """
    Compute p-value using Proportion oracle, i.e., z-test method of 4.1.3 in "A survey on measuring indirect discrimination in machine learning".

    Attributes:
        _data: dataframe that stored the data
        _att: sensitive attribute name
        _protected_group: the value of sensitive attribute for protected group
        _y_col: the column that stores the values of ranking
        top_k: the top ranking to verify group fairness
        round_default: threshold of round function
    Return:  rounded p-value
    """
    
    _data.sort_values(by=_y_col, ascending=False, inplace=True)
    _data.reset_index(drop=True, inplace=True)
    if len(_data)/2 < top_k:
        top_k = int(len(_data)/2)
    total_n = len(_data)
    pro_n = len(_data[_data[_att]==_protected_group])
    unpro_n = total_n - pro_n
    
    top_data = _data.head(top_k)
    pro_k = len(top_data[top_data[_att]==_protected_group])
    unpro_k = top_k - pro_k
    

    pooledSE = math.sqrt((pro_k / pro_n * (1-pro_k/pro_n) / pro_n) + (unpro_k/unpro_n * (1-unpro_k/unpro_n) / unpro_n))
    
    z_test = (unpro_k/unpro_n - pro_k/pro_n) / pooledSE
    p_value = norm.sf(z_test)

    return round(p_value,round_default)

    
def compute_slope_scores(_data, _y_col="Score", round_default=10):
    """
    Compute the slop of a list of scores.

    Attributes:
        _data: file name that stored the data
        _y_col: column name of Y variable
        round_default: threshold of round function for the returned stability
    Return:  slope of scores in the input _data
    """
    xd = [i for i in range(1,len(_data)+1)]
    yd = _data[_y_col].values
    par = np.polyfit(xd, yd, 1, full=True)
    slope = par[0][0]
    return abs(round(slope, round_default))

def is_stable(stability):
    return stability > 0.25

def is_fair(fairness):
    return fairness > 0.05