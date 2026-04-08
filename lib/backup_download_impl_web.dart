// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use
// Web download: same pattern as typical class examples (dart:html).
import 'dart:html' as html;

Future<String?> runStudentBackupDownload(String url, String filename) async {
  html.AnchorElement(href: url)
    ..setAttribute('download', filename)
    ..click();
  return null;
}
