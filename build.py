from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# prepare the train and test data
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y)

# train a model
model = LogisticRegression(max_iter=5000)
model.fit(X_train, y_train)

# convert the model to ONNX
initial_types = [
  ('input', FloatTensorType([None, 4]))
]

onnx_model = convert_sklearn(model, initial_types=initial_types)

# save the model
with open("log_reg_iris.onnx", "wb") as f:
  f.write(onnx_model.SerializeToString())
