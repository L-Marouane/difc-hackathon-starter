-- MRR and MRR movements for the last 18 months
SELECT
  date_format(month, 'yyyy-MM') AS month,
  round(sum(mrr_aed), 0) AS mrr_aed,
  round(sum(new_mrr_aed + expansion_mrr_aed + reactivation_mrr_aed), 0) AS gained_mrr_aed,
  round(sum(churned_mrr_aed + contraction_mrr_aed), 0) AS lost_mrr_aed
FROM workspace.gold.mrr_monthly
WHERE month >= add_months((SELECT max(month) FROM workspace.gold.mrr_monthly), -17)
GROUP BY 1
ORDER BY 1;
