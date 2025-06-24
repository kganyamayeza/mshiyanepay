import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_flutter_project/src/screens/home_screen.dart';

void main() {
  testWidgets('HomeScreen has a title and message', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: HomeScreen()));

    final titleFinder = find.text('Home Screen');
    final messageFinder = find.text('Welcome to the Home Screen!');

    expect(titleFinder, findsOneWidget);
    expect(messageFinder, findsOneWidget);
  });
}