"""Pruebas del código corregido, extraído del notebook."""
import numpy as np
import pandas as pd
import pytest
import app_biopsias as app
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def datos():
    app.rng = np.random.RandomState(app.RANDOM_STATE)
    return app.construir_caracteristicas(app.cargar_datos())


def test_caracteristicas_finitas_y_formula():
    entrada = pd.DataFrame({'mean texture': [18., 18., 18., 18.],
                            'num_biopsias_previas': [0, 1, 2, 3]})
    copia = entrada.copy(deep=True)
    salida = app.construir_caracteristicas(entrada)
    assert np.isfinite(salida['variabilidad_por_biopsia']).all()
    np.testing.assert_allclose(salida['variabilidad_por_biopsia'], [18, 18, 9, 6])
    pd.testing.assert_frame_equal(entrada, copia)


def test_predictores_excluyen_fuga_y_objetivos():
    prohibidas = {'sesiones_tratamiento_programadas', 'diagnostico', 'target'}
    assert prohibidas.isdisjoint(app.COLUMNAS_PREDICTORAS)
    modelo, _, _ = app.entrenar_modelo(datos())
    assert prohibidas.isdisjoint(modelo.feature_names_in_)


def test_predecir_caso_etiquetas_validas():
    df = datos()
    modelo, _, _ = app.entrenar_modelo(df)
    etiquetas = set()
    for _, fila in df[app.COLUMNAS_PREDICTORAS].iterrows():
        etiqueta = app.predecir_caso(modelo, fila.to_dict())
        assert etiqueta in {'benigno', 'maligno'}
        etiquetas.add(etiqueta)
    assert etiquetas == {'benigno', 'maligno'}


@pytest.mark.parametrize('valor', [np.nan, np.inf, -np.inf])
def test_validacion_rechaza_nulos_e_infinitos(valor):
    df = datos()
    df.loc[df.index[0], 'mean texture'] = valor
    with pytest.raises(ValueError, match='Predictores con datos no válidos'):
        app.entrenar_modelo(df)


@pytest.mark.parametrize('balanced', [False, True])
def test_refactor_conserva_predicciones_y_metricas(balanced):
    df = datos()
    X = df[app.COLUMNAS_PREDICTORAS]
    Xtr, Xte, ytr, yte = train_test_split(
        X, df['diagnostico'], test_size=0.25, random_state=app.RANDOM_STATE)
    kwargs = {'max_iter': 5000}
    if balanced:
        kwargs['class_weight'] = 'balanced'
    referencia = LogisticRegression(**kwargs).fit(Xtr, ytr)
    actual, acc_train, acc_test = app.entrenar_modelo(df, balanced)
    np.testing.assert_array_equal(referencia.predict(X), actual.predict(X))
    np.testing.assert_allclose(referencia.coef_, actual.coef_)
    assert acc_train == accuracy_score(ytr, referencia.predict(Xtr))
    assert acc_test == accuracy_score(yte, referencia.predict(Xte))
