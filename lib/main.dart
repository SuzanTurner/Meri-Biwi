import 'package:flutter/material.dart';
import 'widgets/price_calculator.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Meal Plan Calculator',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const Scaffold(
        appBar: AppBar(
          title: Text('Meal Plan Calculator'),
        ),
        body: PriceCalculator(),
      ),
    );
  }
} 