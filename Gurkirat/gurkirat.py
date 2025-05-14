from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Load dataset
iris = load_iris()
X = iris.data       # Features
y = iris.target     # Labels

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Choose a model
model = KNeighborsClassifier()

# Train the model
model.fit(X_train, y_train)

# Test the model
accuracy = model.score(X_test, y_test)
print("Model accuracy:", accuracy)
