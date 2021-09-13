#### Kagle House price Competition:

- Underwent extensive basic cleaning, now streamlined from earlier experiences.
- PCA to reduce features (~80 in basic set)

Two different models were then used, one following the same RF+gridsearch and another venuting into neural networks.

RF achieved slightly improved results (RMSE of 0.17294 vs 0.19117).

In future, I think I'll look to improve both the feature reduction (forward selection instead of PCA?) and the neural network process. 
The current one uses SKlearn's MLPregressor, so either more playing with this, or looking at a different algorithm.
