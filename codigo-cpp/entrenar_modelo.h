#ifndef ENTRENAR_MODELO_H
#define ENTRENAR_MODELO_H

#include <iostream>
#include <mlpack/core.hpp>
#include <mlpack/methods/random_forest/random_forest.hpp>

using namespace mlpack;
using namespace arma;

void entrenar_modelo_mineriadatos()
{
    // 1. Cargar CSV de entrenamiento (features + etiqueta al final)
    arma::mat data;
    data::Load("../csvs/train_features.csv", data, true); // true = transposeIn

    const size_t featureDim = data.n_rows - 1;
    arma::mat X = data.rows(0, featureDim - 1);
    arma::Row<size_t> y =
        arma::conv_to< arma::Row<size_t> >::from(data.row(featureDim));

    // 2. Entrenar Random Forest binario (0 = no vulnerable, 1 = vulnerable)
    const size_t numClasses = 2;
    const size_t numTrees   = 50;
    const size_t minLeafSize = 5;

    mlpack::RandomForest<> rf(X, y, numClasses, numTrees, minLeafSize);

    // Guardar modelo en carpeta modelo/
    data::Save("../modelo/rf_vuln_model.bin", "rf_model", rf, false);

    // 3. Cargar CSV de test
    arma::mat testDataFull;
    data::Load("../csvs/test_features.csv", testDataFull, true);

    arma::mat Xtest = testDataFull.rows(0, featureDim - 1);
    arma::Row<size_t> ytest =
        arma::conv_to< arma::Row<size_t> >::from(testDataFull.row(featureDim));

    // 4. Predicción y guardado
    arma::Row<size_t> predictions;
    rf.Classify(Xtest, predictions);

    predictions.save("../csvs/predictions.csv", arma::csv_ascii);
    
    std::cout << "Modelo entrenado exitosamente.\n";
}

#endif // ENTRENAR_MODELO_H
