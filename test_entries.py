import unittest
import json
import os
import sqlite3
from app import app

class EntryManagementTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        # Create a test database
        self.conn = sqlite3.connect('test_entries.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            content TEXT NOT NULL,
            emotion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()
        
        # Mock the database connection in app.py
        app.config['DB_PATH'] = 'test_entries.db'
    
    def tearDown(self):
        # Close and remove the test database
        self.conn.close()
        os.remove('test_entries.db')
    
    def test_add_entry(self):
        # Test adding an entry
        response = self.app.post('/entries', 
                                json={
                                    'user_id': 'test_user',
                                    'content': 'Test entry content',
                                    'emotion': 'joy'
                                })
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('entry_id', data)
        self.assertEqual(data['message'], 'Entry added successfully')
        
        # Verify the entry was added to the database
        self.cursor.execute('SELECT * FROM entries WHERE user_id = ?', ('test_user',))
        entry = self.cursor.fetchone()
        self.assertIsNotNone(entry)
        self.assertEqual(entry[2], 'Test entry content')
        self.assertEqual(entry[3], 'joy')
    
    def test_get_entries(self):
        # Add a test entry
        self.cursor.execute(
            'INSERT INTO entries (id, user_id, content, emotion) VALUES (?, ?, ?, ?)',
            ('test_id', 'test_user', 'Test entry content', 'joy')
        )
        self.conn.commit()
        
        # Test getting entries
        response = self.app.get('/entries?user_id=test_user')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('entries', data)
        self.assertEqual(len(data['entries']), 1)
        self.assertEqual(data['entries'][0]['id'], 'test_id')
        self.assertEqual(data['entries'][0]['content'], 'Test entry content')
        self.assertEqual(data['entries'][0]['emotion'], 'joy')
    
    def test_remove_entry(self):
        # Add a test entry
        self.cursor.execute(
            'INSERT INTO entries (id, user_id, content, emotion) VALUES (?, ?, ?, ?)',
            ('test_id', 'test_user', 'Test entry content', 'joy')
        )
        self.conn.commit()
        
        # Test removing the entry
        response = self.app.delete('/entries/test_id?user_id=test_user')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Entry removed successfully')
        
        # Verify the entry was removed from the database
        self.cursor.execute('SELECT * FROM entries WHERE id = ?', ('test_id',))
        entry = self.cursor.fetchone()
        self.assertIsNone(entry)
    
    def test_remove_nonexistent_entry(self):
        # Test removing a non-existent entry
        response = self.app.delete('/entries/nonexistent_id?user_id=test_user')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Entry not found or does not belong to the user')

if __name__ == '__main__':
    unittest.main()