from ASR_metrics import utils as metrics

# evaluation
def cacc(lst):
	return 1 - sum(metrics.calculate_cer(mod, new) for (mod, new) in lst) / len(lst)

def wacc(lst):
	return 1 - sum(metrics.calculate_wer(mod, new) for (mod, new) in lst) / len(lst)

