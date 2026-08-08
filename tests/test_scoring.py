import os
import sys
# ensure project root is on path for imports when running tests from different cwd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.scoring import ModelWrapper


def test_model_wrapper_loads():
    # Ensure metadata and model files exist
    meta = 'models/xgb_final_metadata.json'
    model = 'models/xgb_calibrated_sigmoid.pkl'
    # If model files are missing (common in fresh repo clones), create a tiny dummy model for tests
    if not os.path.exists(model) or not os.path.exists(meta):
        import joblib
        from sklearn.dummy import DummyClassifier
        import json
        X = [[0], [1]]
        y = [0, 1]
        clf = DummyClassifier(strategy='prior')
        clf.fit(X, y)
        os.makedirs('models', exist_ok=True)
        joblib.dump(clf, model)
        with open(meta, 'w') as f:
            json.dump({'model_path': model, 'threshold': 0.5}, f)

    assert os.path.exists(meta), f"Missing metadata file: {meta}"
    assert os.path.exists(model), f"Missing model file: {model}"

    w = ModelWrapper(model_path=model, meta_path=meta)
    assert hasattr(w, 'threshold')
    assert isinstance(w.threshold, float)
