import 'package:flutter/material.dart';
import 'dart:ui';
import 'package:home_ease/choose_chef.dart';

class NonDailyPlan extends StatefulWidget {
  const NonDailyPlan({Key? key}) : super(key: key);

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

  Plan({
    required this.name,
    required this.price,
    required this.duration,
    required this.color,
    required this.lightColor,
    required this.features,
    required this.description,
    required this.icon,
  });
}

class _NonDailyPlanState extends State<NonDailyPlan> with TickerProviderStateMixin {
  int _selectedPlanIndex = 1; // Default to Standard plan
  late final TabController _tabController;
  late final AnimationController _animationController;
  late final Animation<double> _fadeAnimation;

  final List<Plan> _plans = [
    Plan(
      name: 'Basic',
      price: '29',
      duration: 'per day',
      color: const Color(0xFF4A9186),
      lightColor: const Color(0xFFE5F5F0),
      features: [
        'One meal per day',
        '8 days/month',
        'Basic Meal options',
        'Standatd ingredients',
        'Next day booking',
      ],
      description: 'Perfect for occasional cooking help with simple meals.',
      icon: Icons.restaurant_outlined,
    ),
    Plan(
      name: 'Standard',
      price: '49',
      duration: 'per day',
      color: const Color(0xFF6A9C89),
      lightColor: const Color(0xFFEFF8F4),
      features: [
        'Two meals per day',
        'Customized menu options',
        'Premium ingredients',
        'Same day booking',
        'Dietary accommodations',
      ],
      description: 'Our most popular plan for quality daily meal.',
      icon: Icons.restaurant_menu,
    ),
    Plan(
      name: 'Premium',
      price: '79',
      duration: 'per day',
      color: const Color(0xFF3C725E),
      lightColor: const Color(0xFFE0F0E9),
      features: [
        'Three meals per day',
        'Gourmet menu options',
        'Organic ingredients',
        'Priority booking',
        'Special dietary needs',
        'Meal planning consultation',
        'Leftover management',
      ],
      description: 'The ultimate experience with gourmet meals.',
      icon: Icons.stars_rounded,
    ),
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(
      length: _plans.length,
      vsync: this,
      initialIndex: _selectedPlanIndex,
    );
    _tabController.addListener(() {
      setState(() {
        _selectedPlanIndex = _tabController.index;
      });
    });

    _animationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _fadeAnimation = CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOut,
    );
    _animationController.forward();
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
                child: const Icon(Icons.help_outline_rounded, color: Color(0xFF6A9C89)),
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
        labelColor: Colors.white,
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
                      child: Icon(plan.icon, color: plan.color, size: 24),
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
                            color: plan.color,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          plan.description,
                          style: TextStyle(
                            fontSize: 12,
                            color: plan.color.withOpacity(0.8),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                ...plan.features.map((feature) => Padding(
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
                            child: Icon(Icons.check, color: plan.color, size: 16),
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
                    )),
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
                    color: plan.color,
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
                          color: plan.color,
                        ),
                      ),
                      Text(
                        plan.price,
                        style: TextStyle(
                          fontSize: 34,
                          fontWeight: FontWeight.bold,
                          color: plan.color,
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
              Container(
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
                      color: plan.color,
                    ),
                    const SizedBox(width: 6),
                    Text(
                      'Terms & Conditions',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                        color: plan.color,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
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
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                    'Selected ${plan.name} plan!',
                  ),
                  backgroundColor: plan.color,
                ),
              );
              Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => ChefProfilesPage()),
    );
            },
            child: Center(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    "Continue with ${plan.name}",
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(width: 8),
                  const Icon(
                    Icons.arrow_forward_rounded,
                    color: Colors.white,
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