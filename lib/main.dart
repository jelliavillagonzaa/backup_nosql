import 'package:flutter/material.dart';

import 'backup_download.dart';

void main() {
  runApp(
    const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: BackupScreen(),
    ),
  );
}

/// MySQL / SQL backup UI — same flow as the instructor’s Mongo example, but your
/// FastAPI uses `mysqldump` and serves `student_backup.gz`.
class BackupScreen extends StatefulWidget {
  const BackupScreen({super.key});

  @override
  State<BackupScreen> createState() => _BackupScreenState();
}

class _BackupScreenState extends State<BackupScreen> {
  String _status = 'Ready to backup SQL database (MySQL via mysqldump)';

  Future<void> _startBackup() async {
    setState(() {
      _status = 'Requesting backup from FastAPI...';
    });

    try {
      const String url = 'http://127.0.0.1:8000/download-student-backup';

      final savedPath =
          await runStudentBackupDownload(url, 'student_backup.gz');

      setState(() {
        _status = savedPath != null
            ? 'Backup saved to:\n$savedPath'
            : 'Backup started! Check your browser downloads folder.';
      });
    } catch (e) {
      setState(() {
        _status =
            'Error: could not reach the server or mysqldump failed. Is FastAPI running?';
      });
      debugPrint('$e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SQL Database Manager'),
        backgroundColor: Colors.teal,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.storage, size: 100, color: Colors.teal),
            const SizedBox(height: 30),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Text(
                _status,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w500,
                ),
                textAlign: TextAlign.center,
              ),
            ),
            const SizedBox(height: 30),
            ElevatedButton.icon(
              onPressed: _startBackup,
              style: ElevatedButton.styleFrom(
                padding:
                    const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                backgroundColor: Colors.teal,
                foregroundColor: Colors.white,
              ),
              icon: const Icon(Icons.play_arrow),
              label: const Text(
                'Click to backup MySQL (student DB)',
                style: TextStyle(fontSize: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
