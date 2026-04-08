import 'dart:io';

import 'package:dio/dio.dart';

Future<String?> runStudentBackupDownload(String url, String filename) async {
  final path =
      '${Directory.systemTemp.path}${Platform.pathSeparator}$filename';
  await Dio().download(url, path);
  return path;
}
