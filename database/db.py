import sqlite3
import json
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path('database/predictions.db')

def init_database():
    """Initialize database with predictions table."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                loc INTEGER NOT NULL,
                wmc REAL NOT NULL,
                rfc REAL NOT NULL,
                cbo REAL NOT NULL,
                lcom REAL NOT NULL,
                code_churn INTEGER NOT NULL,
                num_developers INTEGER NOT NULL,
                past_defects INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                probability REAL NOT NULL,
                confidence REAL NOT NULL,
                prediction TEXT NOT NULL
            )
        ''')
        conn.commit()

@contextmanager
def get_db():
    """Get database connection (context manager)."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def save_prediction(features_dict, result):
    """Save prediction to database."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO predictions (
                    loc, wmc, rfc, cbo, lcom, code_churn, 
                    num_developers, past_defects, risk_level, 
                    probability, confidence, prediction
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                int(features_dict['loc']),
                float(features_dict['wmc']),
                float(features_dict['rfc']),
                float(features_dict['cbo']),
                float(features_dict['lcom']),
                int(features_dict['code_churn']),
                int(features_dict['num_developers']),
                int(features_dict['past_defects']),
                result['risk_level'],
                result['probability'] / 100,  # Store as decimal
                result['confidence'],
                result['prediction']
            ))
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return None

def get_all_predictions(limit=None):
    """Get all predictions from database."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            if limit:
                cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?', (limit,))
            else:
                cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC')
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching predictions: {e}")
        return []

def get_prediction_by_id(pred_id):
    """Get specific prediction by ID."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM predictions WHERE id = ?', (pred_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except Exception as e:
        print(f"Error fetching prediction: {e}")
        return None

def get_prediction_stats():
    """Get statistics about predictions."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Total predictions
            cursor.execute('SELECT COUNT(*) as count FROM predictions')
            total = cursor.fetchone()['count']
            
            # Risk level distribution
            cursor.execute('''
                SELECT risk_level, COUNT(*) as count 
                FROM predictions 
                GROUP BY risk_level
            ''')
            risk_dist = {row['risk_level']: row['count'] for row in cursor.fetchall()}
            
            # Average probability
            cursor.execute('SELECT AVG(probability) as avg_prob FROM predictions')
            avg_prob = cursor.fetchone()['avg_prob'] or 0
            
            # High risk count
            cursor.execute('SELECT COUNT(*) as count FROM predictions WHERE risk_level = ?', ('HIGH',))
            high_risk = cursor.fetchone()['count']
            
            return {
                'total': total,
                'risk_distribution': risk_dist,
                'average_probability': round(avg_prob * 100, 2),
                'high_risk_count': high_risk
            }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {
            'total': 0,
            'risk_distribution': {},
            'average_probability': 0,
            'high_risk_count': 0
        }

def delete_prediction(pred_id):
    """Delete a prediction from database."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM predictions WHERE id = ?', (pred_id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error deleting prediction: {e}")
        return False

def clear_all_predictions():
    """Clear all predictions from database."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM predictions')
            conn.commit()
            return True
    except Exception as e:
        print(f"Error clearing predictions: {e}")
        return False

# Initialize on import
init_database()
