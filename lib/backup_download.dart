import 'backup_download_impl_stub.dart'
    if (dart.library.html) 'backup_download_impl_web.dart' as impl;

/// Web: triggers browser download. Desktop/mobile: saves via HTTP to a temp file.
Future<String?> runStudentBackupDownload(String url, String filename) {
  return impl.runStudentBackupDownload(url, filename);
}
