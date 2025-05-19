import 'package:flutter/material.dart';
import 'package:home_ease/daily_plan_clean.dart';
import 'package:home_ease/your_plan_clean.dart';

class YourDetailsClean extends StatefulWidget {
  const YourDetailsClean({Key? key}) : super(key: key);

  @override
  _YourDetailsCleanState createState() => _YourDetailsCleanState();
}

class _YourDetailsCleanState extends State<YourDetailsClean> with SingleTickerProviderStateMixin {
  // Form state
  int _floorCount = 1;
  int _bhk=2;
  int _bathroomCount= 1;
  
  String _purpose = 'daily';
  bool _BathroomCleaning = false;
  bool _DeepCleaning = false;

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
          'Your Cleaning Details',
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

                  // People Count Card
                  _buildCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSubtitle(
                          'Number of floors',
                          Icons.layers_rounded,
                          isSelected: _floorCount > 0, // Apply gradient if people count is greater than 0
                        ),
                        const SizedBox(height: 16),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.remove_circle_outline, size: 32, color: Color(0xFF2E3C59)),
                              onPressed: _floorCount > 1
                                  ? () => setState(() => _floorCount--)
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
                                  '$_floorCount',
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
                              onPressed: _floorCount < 10
                                  ? () => setState(() => _floorCount++)
                                  : null,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  _buildCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSubtitle(
                          'Number of BHK',
                          Icons.living_outlined,
                          isSelected: _bhk > 0, // Apply gradient if people count is greater than 0
                        ),
                        const SizedBox(height: 16),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.remove_circle_outline, size: 32, color: Color(0xFF2E3C59)),
                              onPressed: _bhk > 1
                                  ? () => setState(() => _bhk--)
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
                                  '$_bhk',
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
                              onPressed: _bhk < 10
                                  ? () => setState(() => _bhk++)
                                  : null,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  _buildCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSubtitle(
                          'Number of Bathroom',
                          Icons.bathroom_rounded,
                          isSelected: _bathroomCount > 0, // Apply gradient if people count is greater than 0
                        ),
                        const SizedBox(height: 16),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.remove_circle_outline, size: 32, color: Color(0xFF2E3C59)),
                              onPressed: _bathroomCount > 1
                                  ? () => setState(() => _bathroomCount--)
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
                                  '$_bathroomCount',
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
                              onPressed: _bathroomCount < 10
                                  ? () => setState(() => _bathroomCount++)
                                  : null,
                            ),
                          ],
                        ),
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
                          isSelected: _BathroomCleaning, // Apply gradient if dishwashing is required
                        ),
                        const SizedBox(height: 16),
                        GestureDetector(
                          onTap: () => setState(() => _BathroomCleaning = !_BathroomCleaning),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(                      
                                color: _BathroomCleaning
                                    ? const Color(0xFF2E3C59)
                                    : Colors.grey.shade300,
                                width: 1.5,
                              ),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  Icons.bubble_chart_outlined,
                                  color: _BathroomCleaning
                                      ? const Color(0xFF2E3C59)
                                      : Colors.grey.shade500,
                                ),
                                const SizedBox(width: 16),
                                const Expanded(
                                  child: Text(
                                    'Bathroom Cleaning',
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                ),
                                Switch(
                                  value: _BathroomCleaning,
                                  onChanged: (value) {
                                    setState(() => _BathroomCleaning = value);
                                  },
                                  activeColor: const Color(0xFFFAFA33)
                                ),
                              ],
                            ),
                          ),
                        ),

                        const SizedBox(height: 16),

                        GestureDetector(
                          onTap: () => setState(() => _DeepCleaning = !_DeepCleaning),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(                      
                                color: _DeepCleaning
                                    ? const Color(0xFF2E3C59)
                                    : Colors.grey.shade300,
                                width: 1.5,
                              ),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  Icons.cleaning_services,
                                  color: _DeepCleaning
                                      ? const Color(0xFF2E3C59)
                                      : Colors.grey.shade500,
                                ),
                                const SizedBox(width: 16),
                                const Expanded(
                                  child: Text(
                                    'Deep Cleaning',
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                ),
                                Switch(
                                  value: _DeepCleaning,
                                  onChanged: (value) {
                                    setState(() => _DeepCleaning = value);
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

                  const SizedBox(height: 36),

                  // Continue Button
                  ElevatedButton(
                    onPressed: () {
                      // Navigate based on the selected purpose
                      if (_purpose == 'daily') {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const DailyPlanClean()),
                        );
                      } else {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const NonDailyPlanClean()),
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