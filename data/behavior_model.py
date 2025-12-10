import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.ensemble import RandomForestClassifier

CSV_PATH = Path("spotify_final_with_behavior.csv")

print(f"Loading {CSV_PATH} ...")
df = pd.read_csv(CSV_PATH)
print("Shape:", df.shape)

# Select features + target
feature_cols_numeric = [
    "spotify_popularity",
    "is_explicit",
    "album_release_year",
    "tempo_bpm_synth",
]
feature_cols_categorical = [
    "time_of_day_synth",
]

target_col = "skipped_synth"

X_num = df[feature_cols_numeric].copy()
X_cat = df[feature_cols_categorical].copy()
y = df[target_col].astype(int)

# One-hot encode categorical
X_cat_dummies = pd.get_dummies(X_cat, columns=feature_cols_categorical, drop_first=False)

X = pd.concat([X_num, X_cat_dummies], axis=1)
print("Final feature columns:", list(X.columns))

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Scale numeric features
scaler = StandardScaler()
X_train_num = scaler.fit_transform(X_train[feature_cols_numeric])
X_test_num = scaler.transform(X_test[feature_cols_numeric])

# Rebuild feature matrices with scaled numeric + raw dummies
X_train_final = pd.concat([
    pd.DataFrame(X_train_num, index=X_train.index, columns=feature_cols_numeric),
    X_train.drop(columns=feature_cols_numeric)
], axis=1)
X_test_final = pd.concat([
    pd.DataFrame(X_test_num, index=X_test.index, columns=feature_cols_numeric),
    X_test.drop(columns=feature_cols_numeric)
], axis=1)

print("X_train_final shape:", X_train_final.shape)

# Train a Random Forest baseline
clf = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced_subsample",
)

print("Training RandomForestClassifier ...")
clf.fit(X_train_final, y_train)

print("Evaluating ...")
y_pred = clf.predict(X_test_final)
y_prob = clf.predict_proba(X_test_final)[:, 1]

print("\nClassification report (0 = not skipped, 1 = skipped):")
print(classification_report(y_test, y_pred, digits=3))

try:
    auc = roc_auc_score(y_test, y_prob)
    print(f"ROC AUC: {auc:.3f}")
except Exception as e:
    print("Could not compute ROC AUC:", e)

print("Done.")
