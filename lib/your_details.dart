import 'package:flutter/material.dart';
import 'package:home_ease/your_plan.dart';
import 'package:home_ease/daily_plan.dart';

class YourDetails extends StatefulWidget {
  const YourDetails({Key? key}) : super(key: key);

  @override
  _YourDetailsState createState() => _YourDetailsState();
}

class _YourDetailsState extends State<YourDetails> with SingleTickerProviderStateMixin {
  // Form state
  String _dietaryPreference = 'vegetarian';
  int _peopleCount = 2;
  final Map<String, bool> _meals = {
    'breakfast': true,
    'lunch': true,
    'dinner': false,
  };
  String _purpose = 'daily';
  //bool _dishwashingRequired = true;
  //bool _childrenSpecial = false;
  bool _kitchenPlatform = false;

  // Animation controller for the slide-in effect
  late AnimationController _animationController;
  late Animation<Offset> _slideAnimation;

  final _gradient = const LinearGradient(
    colors: [
      //Color(0xFFFAFA99), 
      Color(0xFFFAFA33),
      Color(0xFFFAFA33)],
  );

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 600),
    );
    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.2),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOut,
    ));
    _animationController.forward();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFf8f6f0),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        title: const Text(
          'Your Cooking Details',
          style: TextStyle(
            color: Color(0xFF2E3C59),
            fontWeight: FontWeight.bold,
          ),
        ),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Color(0xFF2E3C59)),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: SlideTransition(
        position: _slideAnimation,
        child: FadeTransition(
          opacity: _animationController,
          child: SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 8),
                  _buildSectionTitle('Tell us about your preferences'),
                  const SizedBox(height: 24),

                  // Dietary Preference Card
                  _buildCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSubtitle(
                          'Dietary Preference',
                          Icons.restaurant,
                          isSelected: _dietaryPreference.isNotEmpty, // Apply gradient if any preference is selected
                        ),
                        const SizedBox(height: 16),
                        Row(
                          children: [
                            _buildSelectionButton(
                              label: 'Vegetarian',
                              isSelected: _dietaryPreference == 'vegetarian',
                              onTap: () => setState(() => _dietaryPreference = 'vegetarian'),
                              icon: Icons.spa,
                              gradient: _gradient,
                            ),
                            const SizedBox(width: 16),
                            _buildSelectionButton(
                              label: 'Non-vegetarian',
                              isSelected: _dietaryPreference == 'non-vegetarian',
                              onTap: () => setState(() => _dietaryPreference = 'non-vegetarian'),
                              icon: Icons.restaurant_menu,
                              gradient: _gradient,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  // People Count Card
                  _buildCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSubtitle(
                          'People at Home',
                          Icons.people,
                          isSelected: _peopleCount > 0, // Apply gradient if people count is greater than 0
                        ),
                        const SizedBox(height: 16),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.remove_circle_outline, size: 32, color: Color(0xFF2E3C59)),
                              onPressed: _peopleCount > 1
                                  ? () => setState(() => _peopleCount--)
                                  : null,
                            ),
                            Container(
                              width: 80,
                              height: 60,
                              decoration: BoxDecoration(
                                color: Colors.white,
                                borderRadius: BorderRadius.circular(16),
                                boxShadow: [
                                  BoxShadow(
                                    color: Colors.grey.withOpacity(0.1),
                                    spreadRadius: 1,
                                    blurRadius: 4,
                                    offset: const Offset(0, 2),
                                  ),
                                ],
                              ),
                              child: Center(
                                child: Text(
                                  '$_peopleCount',
                                  style: const TextStyle(
                                    fontSize: 24,
                                    fontWeight: FontWeight.bold,
                                    color: Color(0xFF2E3C59),
                                  ),
                                ),
                              ),
                            ),
                            IconButton(
                              icon: const Icon(Icons.add_circle_outline, size: 32, color: Color(0xFF2E3C59)),
                              onPressed: _peopleCount < 10
                                  ? () => setState(() => _peopleCount++)
                                  : null,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Meals Card
                  _buildCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSubtitle(
                          'Meals per Day',
                          Icons.dining,
                          isSelected: _meals.values.any((element) => element), // Apply gradient if any meal is selected
                        ),
                        const SizedBox(height: 16),
                        Row(
                          children: [
                            _buildMealToggle('Breakfast', 'breakfast', 
                            //Icons.free_breakfast,
                                gradient: _gradient),
                            _buildMealToggle('Lunch', 'lunch', 
                            //Icons.lunch_dining,
                                gradient: _gradient),
                            _buildMealToggle('Dinner', 'dinner', 
                            //Icons.dinner_dining,
                                gradient: _gradient),
                          ],),
                        ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Purpose Card
                  _buildCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSubtitle(
                          'Service Purpose',
                          Icons.calendar_today,
                          isSelected: _purpose.isNotEmpty, // Apply gradient if a purpose is selected
                        ),
                        const SizedBox(height: 16),
                        Row(
                            children: [
                              Expanded(
                              child: _buildPurposeOption('Daily', 'daily', Icons.calendar_view_day,
                                  gradient: _gradient),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: _buildPurposeOption('Weekends', 'weekends', Icons.weekend,
                                  gradient: _gradient),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: _buildPurposeOption('Occasionally', 'occasionally', Icons.event,
                                  gradient: _gradient),
                            ),],
                          ),
                        ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Dishwashing Card
                  _buildCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSubtitle(
                          'Add Services',
                          Icons.add,
                          isSelected: _kitchenPlatform, // Apply gradient if dishwashing is required
                        ),
                        const SizedBox(height: 16),
                        GestureDetector(
                          onTap: () => setState(() => _kitchenPlatform = !_kitchenPlatform),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(                      
                                color: _kitchenPlatform
                                    ? const Color(0xFF2E3C59)
                                    : Colors.grey.shade300,
                                width: 1.5,
                              ),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  Icons.cleaning_services,
                                  color: _kitchenPlatform
                                      ? const Color(0xFF2E3C59)
                                      : Colors.grey.shade500,
                                ),
                                const SizedBox(width: 16),
                                const Expanded(
                                  child: Text(
                                    'Kitchen platform cleaning',
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                ),
                                Switch(
                                  value: _kitchenPlatform,
                                  onChanged: (value) {
                                    setState(() => _kitchenPlatform = value);
                                  },
                                  activeColor: const Color(0xFFFAFA33)
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  
                  /*GestureDetector(
                          onTap: () => setState(() => _dishwashingRequired = !_dishwashingRequired),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(                      
                                color: _dishwashingRequired
                                    ? const Color(0xFF6A9C89)
                                    : Colors.grey.shade300,
                                width: 1.5,
                              ),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  Icons.wash,
                                  color: _dishwashingRequired
                                      ? const Color(0xFF6A9C89)
                                      : Colors.grey.shade500,
                                ),
                                const SizedBox(width: 16),
                                const Expanded(
                                  child: Text(
                                    'Dishwashing',
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                ),
                                Switch(
                                  value: _dishwashingRequired,
                                  onChanged: (value) {
                                    setState(() => _dishwashingRequired = value);
                                  },
                                  activeColor: const Color.fromARGB(255, 29, 95, 70)
                                ),
                              ],
                            ),
                          ),
                        ),
                        //service2
                        const SizedBox(height: 12),
                        GestureDetector(
                          onTap: () => setState(() => _childrenSpecial = !_childrenSpecial),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(                      
                                color: _childrenSpecial
                                    ? const Color(0xFF6A9C89)
                                    : Colors.grey.shade300,
                                width: 1.5,
                              ),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  Icons.lunch_dining_rounded,
                                  color: _childrenSpecial
                                      ? const Color(0xFF6A9C89)
                                      : Colors.grey.shade500,
                                ),
                                const SizedBox(width: 16),
                                const Expanded(
                                  child: Text(
                                    'Children\'s special (1 dish)',
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                ),
                                Switch(
                                  value: _childrenSpecial,
                                  onChanged: (value) {
                                    setState(() => _childrenSpecial = value);
                                  },
                                  activeColor: const Color.fromARGB(255, 29, 95, 70)
                                ),
                              ],
                            ),
                          ),
                        ),
                        //service3
                        //const SizedBox(height: 12),*/
                        

                  const SizedBox(height: 36),

                  // Continue Button
                  ElevatedButton(
                    onPressed: () {
                      // Navigate based on the selected purpose
                      if (_purpose == 'daily') {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const DailyPlan()),
                        );
                      } else {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const NonDailyPlan()),
                        );
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      padding: EdgeInsets.zero,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                    ),
                    child: Ink(
                      decoration: BoxDecoration(
                        gradient: _gradient,
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Container(
                        height: 56,
                        alignment: Alignment.center,
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              'Continue',
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFF2E3C59),
                              ),
                            ),
                            SizedBox(width: 8),
                            Icon(Icons.arrow_forward, color: Color(0xFF2E3C59)),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Text(
      title,
      style: const TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.bold,
        color: Color(0xFF2E3C59),
      ),
    );
  }

  Widget _buildSubtitle(String title, IconData icon, {bool isSelected = false}) {
    return Row(
      children: [
        ShaderMask(
          shaderCallback: (bounds) => isSelected ? _gradient.createShader(bounds) : const LinearGradient(colors: [Colors.grey, Colors.grey]).createShader(bounds),
          child: Icon(icon, color: isSelected ? const Color(0xFF2E3C59) : Colors.grey.shade600),
        ),
        const SizedBox(width: 8),
        Text(
          title,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            color: Color(0xFF2E3C59),
          ),
        ),
      ],
    );
  }

  Widget _buildCard({required Widget child}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.1),
            spreadRadius: 1,
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: child,
    );
  }

  Widget _buildSelectionButton({
    required String label,
    required bool isSelected,
    required VoidCallback onTap,
    required IconData icon,
    required Gradient gradient,
  }) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          padding: const EdgeInsets.symmetric(vertical: 16),
          decoration: BoxDecoration(
            gradient: isSelected ? gradient : null,
            color: isSelected ? null : Colors.white,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: isSelected ? Colors.transparent : Colors.grey.shade300,
              width: 1.5,
            ),
            boxShadow: isSelected
                ? [
                    BoxShadow(
                      color: (gradient.colors.last).withOpacity(0.3),
                      spreadRadius: 1,
                      blurRadius: 8,
                      offset: const Offset(0, 3),
                    ),
                  ]
                : null,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                color: isSelected ? Color(0xFF2E3C59) : Colors.grey.shade600,
                size: 28,
              ),
              const SizedBox(height: 8),
              Text(
                label,
                style: TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w600,
                  color: isSelected ? Color(0xFF2E3C59) : Colors.grey.shade600,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMealToggle(String label, String mealKey,
  // IconData icon, 
  {required Gradient gradient}) {
  final isSelected = _meals[mealKey] ?? false;
  final double fontSize = mealKey == 'breakfast' ? 14 : 15; // Determine fontSize here

  return Expanded(
    child: GestureDetector(
      onTap: () => setState(() => _meals[mealKey] = !isSelected),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
        margin: const EdgeInsets.only(right: 8),
        decoration: BoxDecoration(
          gradient: isSelected ? gradient : null,
          color: isSelected ? null : Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected ? Colors.transparent : Colors.grey.shade300,
            width: 1.5,
          ),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            //Icon( icon,color: isSelected ? Colors.white : Colors.grey.shade600,),
            const SizedBox(width: 8),
            Text(
              label,
              style: TextStyle(
                fontSize: fontSize, // Use the determined fontSize
                fontWeight: FontWeight.w600,
                color: isSelected ? Color(0xFF2E3C59) : Colors.grey.shade600,
              ),
            ),
          ],
        ),
      ),
    ),
  );
}

  Widget _buildPurposeOption(String label, String value, IconData icon, {required Gradient gradient}) {
    final isSelected = _purpose == value;

    return GestureDetector(
      onTap: () => setState(() => _purpose = value),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(vertical: 16),
        decoration: BoxDecoration(
          gradient: isSelected ? gradient : null,
          color: isSelected ? null : Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected ? Colors.transparent : Colors.grey.shade300,
            width: 1.5,
          ),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              color: isSelected ? Color(0xFF2E3C59) : Colors.grey.shade600,
              size: 28,
            ),
            const SizedBox(height: 8),
            Text(
              label,
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: isSelected ? const Color(0xFF2E3C59) : Colors.grey.shade600,
              ),
            ),
          ],
        ),
      ),
    );
  }}