#### Kagle House price Competition:

- Underwent extensive basic cleaning, now streamlined from earlier experiences.
- PCA to reduce features (~80 in basic set)

Two different models were then used, one following the same RF+gridsearch and another venuting into neural networks.

RF achieved slightly improved results against sklearn's untuned neural net(RMSE of 0.17294 vs 0.19117).

Keras' sequence network, once tuned through gridsearchcv improved scores to 0.156
