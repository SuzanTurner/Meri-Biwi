import 'package:flutter/material.dart';
import 'dart:ui';
import 'package:home_ease/choose_chef.dart';

import 'dart:convert';
import 'package:http/http.dart' as http;

class NonDailyPlan extends StatefulWidget {
  final String foodType;
  final int numPeople;
  final Map<String, dynamic>? details;
  final List<String> selectedServices;
  final String planType;
  final String mealType;
  final double basePrice;
  final double totalPrice;

  const NonDailyPlan({
    Key? key,
    required this.foodType,
    required this.numPeople,
    this.details,
    required this.selectedServices,
    required this.planType,
    required this.mealType,
    required this.basePrice,
    required this.totalPrice,
  }) : super(key: key);

  @override
  State<NonDailyPlan> createState() => _NonDailyPlanState();
}

class Plan {
  final String name;
  final String price;
  final String duration;
  final Color color;
  final Color lightColor;
  final List<String> features;
  final String description;
  final IconData icon;
  final List<String> benefits;
  final List<String> pricingIncludes;

  Plan({
    required this.name,
    required this.price,
    required this.duration,
    required this.color,
    required this.lightColor,
    required this.features,
    required this.description,
    required this.icon,
    required this.benefits,
    required this.pricingIncludes,
  });
}

Future<Plan> createPlanFromApi({
  required String name,
  required String foodType,
  required String mealCombo,
  required int numberOfPeople,
  required String planType,
  required String services,
  required Color color,
  required Color lightColor,
  required List<String> features,
  required String description,
  required IconData icon,
  required List<String> benefits,
  required List<String> pricingIncludes,
}) async {
  print('[DEBUG] Creating plan from API for: $name');
  print('[DEBUG] API Parameters:');
  print('- foodType: $foodType');
  print('- mealCombo: $mealCombo');
  print('- numberOfPeople: $numberOfPeople');
  print('- planType: $planType');
  print('- services: $services');

  final uri = Uri.parse('http://127.0.0.1:8000/calculate_total').replace(
    queryParameters: {
      'food_type': foodType,
      'meal_type': mealCombo,
      'num_people': numberOfPeople.toString(),
      'plan_type': planType,
      'services': services,
    },
  );
  print('[DEBUG] API URL: $uri');

  try {
    print('[DEBUG] Making HTTP GET request');
    final response = await http.get(uri);
    print('[DEBUG] Received response with status code: ${response.statusCode}');
    print('[DEBUG] Response body: ${response.body}');

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final price = data['total_price'].toString();
      print('[DEBUG] Successfully parsed price: $price');

      return Plan(
        name: name,
        price: price,
        duration: 'per day',
        color: color,
        lightColor: lightColor,
        features: features,
        description: description,
        icon: icon,
        benefits: benefits,
        pricingIncludes: pricingIncludes,
      );
    } else {
      print('[ERROR] API request failed with status code: ${response.statusCode}');
      throw Exception('Failed to load price for $name');
    }
  } catch (e) {
    print('[ERROR] Exception during API call: $e');
    throw Exception('Failed to load price for $name: $e');
  }
}


class _NonDailyPlanState extends State<NonDailyPlan> with TickerProviderStateMixin {
  int _selectedPlanIndex = 1; // Default to Standard plan
  late final TabController _tabController;
  late final AnimationController _animationController;
  late final Animation<double> _fadeAnimation;

  List<Plan> _plans = [];

  @override
  void initState() {
    print('[DEBUG] Initializing NonDailyPlan widget');
    print('[DEBUG] Received parameters:');
    print('- foodType: ${widget.foodType}');
    print('- numPeople: ${widget.numPeople}');
    print('- selectedServices: ${widget.selectedServices}');
    print('- planType: ${widget.planType}');
    print('- mealType: ${widget.mealType}');
    print('- details: ${widget.details}');
    
    super.initState();
    _tabController = TabController(
      length: 3,
      vsync: this,
      initialIndex: _selectedPlanIndex,
    );
    print('[DEBUG] TabController initialized with length: 3, initialIndex: $_selectedPlanIndex');
    
    _tabController.addListener(() {
      print('[DEBUG] Tab changed to index: ${_tabController.index}');
      setState(() {
        _selectedPlanIndex = _tabController.index;
      });
    });

    _animationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    print('[DEBUG] AnimationController initialized');
    
    _fadeAnimation = CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOut,
    );
    print('[DEBUG] FadeAnimation initialized');
    
    _animationController.forward();
    print('[DEBUG] Animation started');

    loadPlans();
  }

  void loadPlans() async {
    print('[DEBUG] Starting loadPlans()');
    final List<Plan> fetchedPlans = [];

    final Map<String, dynamic> params = {
      'foodType': widget.foodType,
      'mealCombo': widget.mealType,
      'numberOfPeople': widget.numPeople,
      'services': widget.selectedServices.isNotEmpty ? widget.selectedServices.join(',') : '',
    };
    print('[DEBUG] API Parameters: $params');

    final List<String> planTypes = ['Basic', 'Standard', 'Premium'];
    print('[DEBUG] Processing plan types: $planTypes');

    for (String planType in planTypes) {
      print('[DEBUG] Processing plan type: $planType');
      try {
        print('[DEBUG] Making API call for $planType plan');
        final plan = await createPlanFromApi(
          name: planType,
          foodType: params['foodType'] as String,
          mealCombo: params['mealCombo'] as String,
          numberOfPeople: params['numberOfPeople'] as int,
          planType: planType,
          services: params['services'] as String,
          color: const Color(0xFFFAFA33),
          lightColor: const Color(0xFFFEF54A).withOpacity(0.15),
          features: getFeaturesFor(planType),
          description: getDescriptionFor(planType),
          icon: getIconFor(planType),
          benefits: getBenefitsFor(planType),
          pricingIncludes: getPricingIncludesFor(planType),
        );
        print('[DEBUG] Successfully created plan for $planType with price: ${plan.price}');
        fetchedPlans.add(plan);
        
        // Update state after each successful plan fetch
        if (mounted) {
          setState(() {
            _plans = List.from(fetchedPlans);
          });
          print('[DEBUG] Updated state with new plan: $planType (${plan.price})');
        }
      } catch (e) {
        print('[ERROR] Failed to load plan $planType: $e');
        print('[DEBUG] Creating fallback plan for $planType');
        final fallbackPlan = Plan(
          name: planType,
          price: '0',
          duration: 'per day',
          color: const Color(0xFFFAFA33),
          lightColor: const Color(0xFFFEF54A).withOpacity(0.15),
          features: getFeaturesFor(planType),
          description: getDescriptionFor(planType),
          icon: getIconFor(planType),
          benefits: getBenefitsFor(planType),
          pricingIncludes: getPricingIncludesFor(planType),
        );
        print('[DEBUG] Fallback plan created for $planType');
        fetchedPlans.add(fallbackPlan);
        
        // Update state after each fallback plan
        if (mounted) {
          setState(() {
            _plans = List.from(fetchedPlans);
          });
          print('[DEBUG] Updated state with fallback plan: $planType');
        }
      }
    }

    print('[DEBUG] All plans processed. Total plans: ${fetchedPlans.length}');
    if (mounted) {
      print('[DEBUG] Final state update with all plans');
      setState(() {
        _plans = fetchedPlans;
      });
      print('[DEBUG] Final state updated with all plans');
    } else {
      print('[WARNING] Widget is not mounted, skipping final state update');
    }
  }

  // Helper functions with logging
  List<String> getFeaturesFor(String planType) {
    print('[DEBUG] Getting features for plan type: $planType');
    final features = switch (planType) {
      'Basic' => <String>[
          'One meal per day for weekends',
          'Standard dishes',
          'Preset menu only',
          'Spicy customization',
        ],
      'Standard' => <String>[
          'Two meals per day for weekdays',
          'Semi-custom menu',
          'Sweets/snacks included',
          'Access to festive menu',
          'Weekly menu rotation',
          'Customer support',
        ],
      'Premium' => <String>[
          'Three meals daily all week',
          'Fully customizable',
          'Chef-designed menus',
          'Priority support',
          'Desserts & snacks daily',
          'Festive menus included',
          'Nutrition tracking',
          'Flexible pause option',
        ],
      _ => <String>[],
    };
    print('[DEBUG] Retrieved ${features.length} features for $planType');
    return features;
  }

  String getDescriptionFor(String planType) {
    print('[DEBUG] Getting description for plan type: $planType');
    final description = switch (planType) {
      'Basic' => 'Perfect for light weekend meals with simplicity.',
      'Standard' => 'A balanced meal solution for busy families.',
      'Premium' => 'Best suited for gourmet-style daily meals.',
      _ => '',
    };
    print('[DEBUG] Retrieved description for $planType: $description');
    return description;
  }

  IconData getIconFor(String planType) {
    print('[DEBUG] Getting icon for plan type: $planType');
    final icon = switch (planType) {
      'Basic' => Icons.restaurant_outlined,
      'Standard' => Icons.restaurant_menu,
      'Premium' => Icons.stars_rounded,
      _ => Icons.restaurant,
    };
    print('[DEBUG] Retrieved icon for $planType');
    return icon;
  }

  List<String> getBenefitsFor(String planType) {
    print('[DEBUG] Getting benefits for plan type: $planType');
    final benefits = switch (planType) {
      'Basic' => <String>[
          'Affordable pricing',
          'Simple service',
          'Quick setup',
        ],
      'Standard' => <String>[
          'More variety',
          'Healthy combinations',
          'Reliable scheduling',
        ],
      'Premium' => <String>[
          'Maximum flexibility',
          'Rich culinary experience',
          'Premium customer care',
        ],
      _ => <String>[],
    };
    print('[DEBUG] Retrieved ${benefits.length} benefits for $planType');
    return benefits;
  }

  List<String> getPricingIncludesFor(String planType) {
    print('[DEBUG] Getting pricing includes for plan type: $planType');
    final pricingIncludes = switch (planType) {
      'Basic' => <String>[
          'Includes GST',
          'No hidden charges',
          'Free weekend delivery',
        ],
      'Standard' => <String>[
          'Includes GST',
          'Free rescheduling x2/month',
          'Doorstep delivery',
        ],
      'Premium' => <String>[
          'Includes GST',
          'Priority chef availability',
          'No additional service fee',
        ],
      _ => <String>[],
    };
    print('[DEBUG] Retrieved ${pricingIncludes.length} pricing includes for $planType');
    return pricingIncludes;
  }

  @override
  void dispose() {
    _tabController.dispose();
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      backgroundColor: const Color(0xFFF8F6F0),
      body: SafeArea(
        child: FadeTransition(
          opacity: _fadeAnimation,
          child: Column(
            children: [
              _buildHeader(),
              Expanded(
                child: SingleChildScrollView(
                  physics: const BouncingScrollPhysics(),
                  child: Column(
                    children: [
                      _buildPlanTabs(),
                      AnimatedSwitcher(
                        duration: const Duration(milliseconds: 400),
                        transitionBuilder: (Widget child, Animation<double> animation) {
                          return FadeTransition(
                            opacity: animation,
                            child: SlideTransition(
                              position: Tween<Offset>(
                                begin: const Offset(0.03, 0),
                                end: Offset.zero,
                              ).animate(animation),
                              child: child,
                            ),
                          );
                        },
                        child: _buildPlanDetails(key: ValueKey(_selectedPlanIndex)),
                      ),
                      const SizedBox(height: 20),
                      _buildPricingCard(),
                      const SizedBox(height: 30),
                    ],
                  ),
                ),
              ),
              _buildBottomButton(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              IconButton(
                icon: const Icon(Icons.arrow_back_ios_rounded, color: Color(0xFF2D3A3A)),
                padding: EdgeInsets.zero,
                constraints: const BoxConstraints(),
                onPressed: () {
                  // Handle back navigation
                },
              ),
              const Spacer(),
              Container(
                height: 40,
                width: 40,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(12),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.05),
                      blurRadius: 10,
                      offset: const Offset(0, 2),
                    ),
                  ],
                ),
                //child: const Icon(Icons.help_outline_rounded, color: Color(0xFFFAFA33)),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Text(
            "Select Your Plan",
            style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                  fontSize: 28,
                ),
          ),
          const SizedBox(height: 8),
          Text(
            "Choose the perfect cooking plan for your needs",
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: const Color(0xFF5C6E6E),
                  fontSize: 16,
                ),
          ),
        ],
      ),
    );
  }

  Widget _buildPlanTabs() {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: TabBar(
        controller: _tabController,
        indicator: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          color: _plans[_selectedPlanIndex].color,
        ),
        labelColor: Color(0xFF2E3C59),
        unselectedLabelColor: const Color(0xFF5C6E6E),
        labelStyle: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
        unselectedLabelStyle: const TextStyle(fontWeight: FontWeight.w500, fontSize: 16),
        tabs: _plans
            .map((plan) => Tab(
                  height: 60,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(plan.icon, size: 18),
                      const SizedBox(width: 8),
                      Text(plan.name),
                    ],
                  ),
                ))
            .toList(),
      ),
    );
  }

  Widget _buildPlanDetails({Key? key}) {
    final plan = _plans[_selectedPlanIndex];
    
    return Padding(
      key: key,
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 24),
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: plan.lightColor,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: plan.color.withOpacity(0.3), width: 1),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: plan.color.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Icon(plan.icon, color: Color(0xFF2E3C59), size: 24),
                    ),
                    const SizedBox(width: 12),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          plan.name,
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w600,
                            color: const Color(0xFF2E3C59),
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          plan.description,
                          style: TextStyle(
                            fontSize: 12,
                            color: const Color(0xFF2E3C59).withOpacity(0.8),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                ...plan.features.map((feature) {
                  final isSpicyCustomization = feature == 'Spicy customization';
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                      child: Row(
                        children: [
                          Container(
                            height: 24,
                            width: 24,
                            decoration: BoxDecoration(
                              color: plan.color.withOpacity(0.2),
                              shape: BoxShape.circle,
                            ),
                            child: Icon(
                              isSpicyCustomization ? Icons.close : Icons.check,
                              color: isSpicyCustomization ? Colors.red : Color(0xFF2E3C59),
                              size: 16,
                            ),
                          ),
                          const SizedBox(width: 12),
                          Text(
                            feature,
                            style: TextStyle(
                              fontSize: 15,
                              color: Colors.black.withOpacity(0.7),
                            ),
                          ),
                        ],
                      ),
                    );
                }),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPricingCard() {
    final plan = _plans[_selectedPlanIndex];
    
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: plan.color.withOpacity(0.15),
            blurRadius: 20,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Plan Summary',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: Colors.black.withOpacity(0.8),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: plan.lightColor,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  plan.name,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: const Color(0xFF2E3C59),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Divider(height: 1),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Total Price',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.black.withOpacity(0.6),
                    ),
                  ),
                  const SizedBox(height: 4),
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '\₹',
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.w600,
                          color: Color(0xFF2E3C59),
                        ),
                      ),
                      Text(
                        plan.price,
                        style: TextStyle(
                          fontSize: 34,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF2E3C59),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.only(top: 8.0),
                        child: Text(
                          ' ${plan.duration}',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.black.withOpacity(0.6),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
              GestureDetector(
                onTap: () {
                  _showTermsAndConditions(context);
                },
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  decoration: BoxDecoration(
                    color: plan.color.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Row(
                    children: [
                      Icon(
                        Icons.edit_document,
                        size: 16,
                        color: Color(0xFF2E3C59),
                      ),
                      const SizedBox(width: 6),
                      Text(
                        'Terms & Conditions',
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w500,
                          color: Color(0xFF2E3C59),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  void _showTermsAndConditions(BuildContext context) {
    final plan = _plans[_selectedPlanIndex];
    
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) {
          return Container(
            height: MediaQuery.of(context).size.height * 0.85,
            decoration: const BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(24),
                topRight: Radius.circular(24),
              ),
            ),
            child: Column(
              children: [
                // Handle bar
                Container(
                  margin: const EdgeInsets.only(top: 12),
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: Colors.grey.withOpacity(0.3),
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
                // Header
                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 20, 20, 0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "${plan.name} Plan",
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF2E3C59),
                        ),
                      ),
                      IconButton(
                        onPressed: () => Navigator.pop(context),
                        icon: const Icon(Icons.close, size: 24),
                        color: Colors.grey[600],
                      ),
                    ],
                  ),
                ),
                const Divider(height: 24),
                // Content
                Expanded(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          plan.description,
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.grey[700],
                          ),
                        ),
                        const SizedBox(height: 24),
                        
                        // Features
                        _buildTermSection(
                          title: "Features",
                          icon: Icons.check_circle_outline,
                          color: Color(0xFF2E3C59),
                          items: plan.features,
                        ),
                        
                        // Benefits
                        _buildTermSection(
                          title: "Benefits",
                          icon: Icons.star_outline,
                          color: Color(0xFF2E3C59),
                          items: plan.benefits,
                        ),
                        
                        // Pricing Includes
                        _buildTermSection(
                          title: "Pricing Includes",
                          icon: Icons.receipt_long,
                          color: Color(0xFF2E3C59),
                          items: plan.pricingIncludes,
                        ),
                        
                        const SizedBox(height: 24),
                        
                        // Additional T&C
                        _buildTermsParagraph(
                          title: "Payment Terms",
                          content: "Payment is to be made in advance for the selected plan duration. All prices are inclusive of applicable taxes. Refunds are processed as per our refund policy within 7 working days.",
                        ),
                        
                        _buildTermsParagraph(
                          title: "Cancellation Policy",
                          content: "Customers can cancel their subscription with 48 hours notice. Pro-rated refunds will be processed for unused days. Cancellation fees may apply as per the plan terms.",
                        ),
                        
                        _buildTermsParagraph(
                          title: "Service Delivery",
                          content: "HomeEase guarantees timely delivery of meals as per the schedule agreed upon. In case of unavoidable delays, customers will be notified in advance.",
                        ),
                        
                        const SizedBox(height: 36),
                      ],
                    ),
                  ),
                ),
                // Button
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.05),
                        blurRadius: 10,
                        offset: const Offset(0, -3),
                      ),
                    ],
                  ),
                  child: ElevatedButton(
                    onPressed: () {
                      Navigator.pop(context);
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: plan.color,
                      foregroundColor: Color(0xFF2E3C59),
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                    ),
                    child: Text(
                      "Confirm ${plan.name} Plan",
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildTermSection({
    required String title,
    required IconData icon,
    required Color color,
    required List<String> items,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, color: color, size: 20),
            const SizedBox(width: 8),
            Text(
              title,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w600,
                color: color,
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        ...items.map((item) => Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                "• ",
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: color,
                ),
              ),
              Expanded(
                child: Text(
                  item,
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.grey[700],
                  ),
                ),
              ),
            ],
          ),
        )),
        const SizedBox(height: 20),
      ],
    );
  }

  Widget _buildTermsParagraph({required String title, required String content}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: Colors.grey[800],
          ),
        ),
        const SizedBox(height: 8),
        Text(
          content,
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey[600],
            height: 1.5,
          ),
        ),
        const SizedBox(height: 16),
      ],
    );
  }

  Widget _buildBottomButton() {
    final plan = _plans[_selectedPlanIndex];
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, -3),
          ),
        ],
      ),
      child: Container(
        width: double.infinity,
        height: 60,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [plan.color, plan.color.withOpacity(0.8)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: plan.color.withOpacity(0.3),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            borderRadius: BorderRadius.circular(16),
            onTap: () {
              // Handle continue button tap
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ChefProfilesPage(
                    totalPrice: widget.totalPrice,
                  ),
                ),
              );
            },
            child: Center(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    "Continue with ${plan.name}",
                    style: const TextStyle(
                      color: Color(0xFF2E3C59),
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(width: 8),
                  const Icon(
                    Icons.arrow_forward_rounded,
                    color: Color(0xFF2E3C59),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}