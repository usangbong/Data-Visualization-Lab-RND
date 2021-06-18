import pysaliency

dataset_location = 'datasets'
model_location = 'models'

mit_stimuli, mit_fixations = pysaliency.external_datasets.get_mit1003(location=dataset_location)
aim = pysaliency.AIM(location=model_location)
saliency_map = aim.saliency_map(mit_stimuli.stimuli[0])

plt.imshow(saliency_map)

auc = aim.AUC(mit_stimuli, mit_fixations)
