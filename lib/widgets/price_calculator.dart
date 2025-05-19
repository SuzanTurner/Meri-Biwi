import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PriceCalculator extends StatefulWidget {
  const PriceCalculator({super.key});

  @override
  State<PriceCalculator> createState() => _PriceCalculatorState();
}

class _PriceCalculatorState extends State<PriceCalculator> {
  final _formKey = GlobalKey<FormState>();
  String _foodType = 'VEG';
  String _planType = 'BASIC';
  String _mealType = 'BREAKFAST';
  int _numPeople = 1;
  List<String> _selectedServices = [];
  Map<String, dynamic>? _priceDetails;
  bool _isLoading = false;

  // Update this to your machine's IP address when running on mobile/emulator
  final String _baseUrl = 'http://10.0.2.2:8000'; // Use this for Android emulator
  // final String _baseUrl = 'http://localhost:8000'; // Use this for web/desktop

  final List<String> _foodTypes = ['VEG', 'NON_VEG'];
  final List<String> _planTypes = ['BASIC', 'STANDARD', 'PREMIUM'];
  final List<String> _mealTypes = ['BREAKFAST', 'LUNCH', 'DINNER', 'BREAKFAST_LUNCH', 'BREAKFAST_LUNCH_DINNER'];
  final List<String> _services = ['A', 'B', 'C', 'D']; // Add your service codes here

  Future<void> _calculatePrice() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _priceDetails = null;
    });

    try {
      final queryParams = {
        'food_type': _foodType,
        'plan_type': _planType,
        'num_people': _numPeople.toString(),
        'meal_type': _mealType,
        ..._selectedServices.asMap().map((i, service) => MapEntry('services[$i]', service)),
      };

      final uri = Uri.parse('$_baseUrl/calculate-total').replace(queryParameters: queryParams);
      final response = await http.get(uri);

      if (response.statusCode == 200) {
        setState(() {
          _priceDetails = json.decode(response.body);
        });
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error: ${response.body}')),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            DropdownButtonFormField<String>(
              value: _foodType,
              decoration: const InputDecoration(labelText: 'Food Type'),
              items: _foodTypes.map((type) {
                return DropdownMenuItem(
                  value: type,
                  child: Text(type),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _foodType = value!;
                });
              },
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _planType,
              decoration: const InputDecoration(labelText: 'Plan Type'),
              items: _planTypes.map((type) {
                return DropdownMenuItem(
                  value: type,
                  child: Text(type),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _planType = value!;
                });
              },
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _mealType,
              decoration: const InputDecoration(labelText: 'Meal Type'),
              items: _mealTypes.map((type) {
                return DropdownMenuItem(
                  value: type,
                  child: Text(type),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _mealType = value!;
                });
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: '1',
              decoration: const InputDecoration(labelText: 'Number of People'),
              keyboardType: TextInputType.number,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter number of people';
                }
                final num = int.tryParse(value);
                if (num == null || num < 1 || num > 7) {
                  return 'Please enter a number between 1 and 7';
                }
                return null;
              },
              onChanged: (value) {
                setState(() {
                  _numPeople = int.parse(value);
                });
              },
            ),
            const SizedBox(height: 16),
            const Text('Additional Services:'),
            Wrap(
              spacing: 8.0,
              children: _services.map((service) {
                return FilterChip(
                  label: Text(service),
                  selected: _selectedServices.contains(service),
                  onSelected: (selected) {
                    setState(() {
                      if (selected) {
                        _selectedServices.add(service);
                      } else {
                        _selectedServices.remove(service);
                      }
                    });
                  },
                );
              }).toList(),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _isLoading ? null : _calculatePrice,
              child: _isLoading
                  ? const CircularProgressIndicator()
                  : const Text('Calculate Price'),
            ),
            if (_priceDetails != null) ...[
              const SizedBox(height: 24),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Price Details',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      const SizedBox(height: 16),
                      Text('Base Price: ₹${_priceDetails!['base_price']}'),
                      Text('Total Price: ₹${_priceDetails!['total_price']}'),
                      Text('Number of People: ${_priceDetails!['num_people']}'),
                      Text('Food Type: ${_priceDetails!['food_type']}'),
                      Text('Plan Type: ${_priceDetails!['plan_type']}'),
                      Text('Meal Type: ${_priceDetails!['meal_type']}'),
                      if (_priceDetails!['services'].isNotEmpty)
                        Text('Selected Services: ${_priceDetails!['services'].join(', ')}'),
                    ],
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
} 