import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:home_ease/booking_summary.dart';

class ChefProfilesPage extends StatefulWidget {
  const ChefProfilesPage({Key? key}) : super(key: key);

  @override
  _ChefProfilesPageState createState() => _ChefProfilesPageState();
}

class _ChefProfilesPageState extends State<ChefProfilesPage> with SingleTickerProviderStateMixin {
  // Chef preferences state
  DateTime _startDate = DateTime.now().add(const Duration(days: 1));
  String _genderPreference = 'Female';
  String _timePreference = 'any';
  String _communityPreference = 'any';
  bool _showPeakHours = false;
  
  // Animation controller for scrolling effects
  late AnimationController _animationController;
  
  
  // Mock data for chefs
  List<Map<String, dynamic>> _chefs = [];
  bool _isLoading = false;
  int _currentPage = 0;
  
  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
    
    
    // Show preferences dialog after build
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _showPreferencesDialog();
    });
    
    // Initialize with first batch of chefs
    _loadChefs();
  }
  
 
  
  void _loadChefs() {
  if (_isLoading) return;

  setState(() {
    _isLoading = true;
  });

  // Simulate API call with delay
  Future.delayed(const Duration(milliseconds: 800), () {
    // Generate some mock chef data using local assets
    final newChefs = List.generate(8, (index) {
      final actualIndex = _currentPage * 8 + index;
      return {
        'id': actualIndex,
        'name': 'Chef ${_getRandomName()}',
        'image': 'assets/chefs/person icon.jpeg', // Assuming you have at least 10 chef images
        'rating': 3.5 + (actualIndex % 3) * 0.5,
        'speciality': _getRandomSpeciality(),
        'experience': '${2 + (actualIndex % 15)} years',
        'bio': 'Passionate chef specializing in ${_getRandomSpeciality()}. '
            'Bringing creative flavors to your table with attention to detail '
            'and culinary excellence.',
        'languages': _getRandomLanguages(),
      };
    });

    setState(() {
      _chefs.addAll(newChefs);
      _currentPage++;
      _isLoading = false;
    });
  });
}
  
  // Mock data generators
  String _getRandomName() {
    final names = ['Sarah', 'Michael', 'Priya', 'Raj', 'Emma', 'Ahmed', 'Liu', 'Isabella', 'Jamal', 'Sophia', 'Arjun', 'Maria'];
    final surnames = ['Smith', 'Patel', 'Wong', 'Ali', 'Johnson', 'Kumar', 'Garcia', 'Chen', 'Rossi', 'Singh', 'Lopez', 'Sato'];
    return '${names[DateTime.now().microsecond % names.length]} ${surnames[DateTime.now().millisecond % surnames.length]}';
  }
  
  String _getRandomSpeciality() {
    final specialities =[
  'Jain',
  'Marwadi',
  'Hindu',
  'Muslim',
  'Parsi',
  'Christian',
  'Buddhist'
];
    return specialities[DateTime.now().millisecond % specialities.length];
  }
  
  List<String> _getRandomLanguages() {
    final allLanguages = ['English', 'Hindi', 'Marathi','Gujrati', 'Arbi', 'Telugu'];
    final count = 1 + (DateTime.now().millisecond % 3);
    final languages = <String>[];
    
    for (int i = 0; i < count; i++) {
      final language = allLanguages[DateTime.now().microsecond % allLanguages.length];
      if (!languages.contains(language)) {
        languages.add(language);
      }
    }
    
    return languages;
  }
  
  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }
  
  void _showPreferencesDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => PreferencesDialog(
        onSubmit: (startDate, gender, timePreference, community, showPeakHours) {
          setState(() {
            _startDate = startDate;
            _genderPreference = gender;
            _timePreference = timePreference;
            _communityPreference = community;
            _showPeakHours = showPeakHours;
            
            // Reset and reload chefs based on new preferences
            _chefs = [];
            _currentPage = 0;
            _loadChefs();
          });
        },
      ),
    );
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 62, 113, 93),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.white,
        title: const Text(
          'Find Your Chef',
          style: TextStyle(
            color: Color(0xFF2E3C59),
            fontWeight: FontWeight.bold,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.tune, color: Color.fromARGB(255, 62, 113, 93)),
            onPressed: _showPreferencesDialog,
            tooltip: 'Chef Preferences',
          ),
        ],
      ),
      body: Column(
        children: [
          // Active filters display
          if (_genderPreference != 'any' || _timePreference != 'any' || _communityPreference != 'any')
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              color: Colors.white,
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [
                    _filterChip(
                      label: 'Date: ${DateFormat('MMM d, yyyy').format(_startDate)}',
                      icon: Icons.calendar_today,
                    ),
                    if (_genderPreference != 'any')
                      _filterChip(
                        label: 'Gender: ${_genderPreference[0].toUpperCase() + _genderPreference.substring(1)}',
                        icon: _genderPreference == 'male' ? Icons.male : Icons.female,
                      ),
                    if (_timePreference != 'any')
                      _filterChip(
                        label: 'Time: ${_timePreference[0].toUpperCase() + _timePreference.substring(1)}',
                        icon: Icons.access_time,
                      ),
                    if (_communityPreference != 'any')
                      _filterChip(
                        label: 'Community: ${_communityPreference[0].toUpperCase() + _communityPreference.substring(1)}',
                        icon: Icons.people,
                      ),
                    if (_showPeakHours)
                      _filterChip(
                        label: 'Peak Hours',
                        icon: Icons.trending_up,
                        color: Colors.amber[700],
                      ),
                  ],
                ),
              ),
            ),
          
          // Chef grid
          Expanded(
            child: LayoutBuilder(
              builder: (context, constraints) {
                // Determine number of columns based on screen width
                final double width = constraints.maxWidth;
                int crossAxisCount = 2; // Default for phones
                
                if (width > 600) crossAxisCount = 3; // Tablets
                if (width > 900) crossAxisCount = 4; // Large tablets/desktop
                
                return RefreshIndicator(
                  onRefresh: () async {
                    setState(() {
                      _chefs = [];
                      _currentPage = 0;
                    });
                    _loadChefs();
                  },
                  color: const Color.fromARGB(255, 62, 113, 93),
                  child: CustomScrollView(
                    physics: const AlwaysScrollableScrollPhysics(),
                    slivers: [
                      SliverPadding(
                        padding: const EdgeInsets.all(16),
                        sliver: SliverGrid(
                          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: crossAxisCount,
                            childAspectRatio: 0.75,
                            crossAxisSpacing: 16,
                            mainAxisSpacing: 16,
                          ),
                          delegate: SliverChildBuilderDelegate(
                            (context, index) {
                              if (index >= _chefs.length) {
                                return null;
                              }
                              
                              final chef = _chefs[index];
                              
                              // Add staggered animation to chef cards
                              return AnimatedBuilder(
                                animation: _animationController,
                                builder: (context, child) {
                                  // Calculate delay based on position
                                  final delay = index % (crossAxisCount * 2) * 0.1;
                                  final animation = CurvedAnimation(
                                    parent: _animationController,
                                    curve: Interval(
                                      delay,
                                      delay + 0.8,
                                      curve: Curves.easeOutQuart,
                                    ),
                                  );
                                  
                                  _animationController.forward();
                                  
                                  return FadeTransition(
                                    opacity: animation,
                                    child: SlideTransition(
                                      position: Tween<Offset>(
                                        begin: const Offset(0, 0.2),
                                        end: Offset.zero,
                                      ).animate(animation),
                                      child: child,
                                    ),
                                  );
                                },
                                child: _buildChefCard(chef),
                              );
                            },
                          ),
                        ),
                      ),
                      SliverToBoxAdapter(
                        child: _isLoading
                            ? Container(
                                padding: const EdgeInsets.all(16.0),
                                alignment: Alignment.center,
                                child: const CircularProgressIndicator(
                                  valueColor: AlwaysStoppedAnimation<Color>(Color.fromARGB(255, 62, 113, 93)),
                                ),
                              )
                            : const SizedBox.shrink(),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _filterChip({required String label, required IconData icon, Color? color}) {
    return Container(
      margin: const EdgeInsets.only(right: 8),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color ?? const Color(0xFFEDF7ED),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: color != null ? color.withOpacity(0.3) : const Color.fromARGB(255, 62, 113, 93).withOpacity(0.3),
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            size: 16,
            color: color ?? const Color.fromARGB(255, 62, 113, 93),
          ),
          const SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              color: color ?? const Color.fromARGB(255, 62, 113, 93),
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildChefCard(Map<String, dynamic> chef) {
    return GestureDetector(
      onTap: () => _showChefDetails(chef),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Chef image
            Expanded(
  flex: 5,
  child: Container(
    decoration: BoxDecoration(
      borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
      image: DecorationImage(
        image: AssetImage(chef['image']), // Use AssetImage here
        fit: BoxFit.cover,
      ),
    ),
                child: Stack(
                  children: [
                    // Add peak hour badge if applicable
                    if (_showPeakHours && chef['id'] % 3 == 0)
                      Positioned(
                        top: 8,
                        right: 8,
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.amber[700],
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(
                                Icons.bolt,
                                color: Colors.white,
                                size: 14,
                              ),
                              SizedBox(width: 2),
                              Text(
                                'Peak',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                  ],
                ),
              ),
            ),
            // Chef info
            Expanded(
              flex: 3,
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      chef['name'],
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      chef['speciality'],
                      style: TextStyle(
                        color: Colors.grey[600],
                        fontSize: 12,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    Row(
                      children: [
                        RatingBar.builder(
                          initialRating: chef['rating'],
                          minRating: 1,
                          direction: Axis.horizontal,
                          allowHalfRating: true,
                          itemCount: 5,
                          itemSize: 14,
                          ignoreGestures: true,
                          itemBuilder: (context, _) => const Icon(
                            Icons.star,
                            color: Colors.amber,
                          ),
                          onRatingUpdate: (rating) {},
                        ),
                        const SizedBox(width: 4),
                        Text(
                          chef['rating'].toString(),
                          style: const TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  void _showChefDetails(Map<String, dynamic> chef) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.6,
        minChildSize: 0.5,
        maxChildSize: 0.9,
        builder: (context, scrollController) {
          return Container(
            decoration: const BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
            ),
            child: Stack(
              children: [
                SingleChildScrollView(
                  controller: scrollController,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // Chef header with image
                      Stack(
                        clipBehavior: Clip.none,
                        children: [
                          // Banner background
                          Container(
                            height: 120,
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                colors: [
                                  const Color.fromARGB(255, 62, 113, 93),
                                  const Color.fromARGB(255, 62, 113, 93).withOpacity(0.7),
                                ],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ),
                              borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
                            ),
                          ),
                          // Chef image
                          Positioned(
  left: 20,
  top: 60,
  child: Container(
    decoration: BoxDecoration(
      shape: BoxShape.circle,
      border: Border.all(color: Colors.white, width: 4),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withOpacity(0.1),
          blurRadius: 10,
          spreadRadius: 2,
        ),
      ],
    ),
    child: CircleAvatar(
      radius: 60,
      backgroundImage: AssetImage(chef['image']), // Use AssetImage here
    ),
  ),
),
                          
                          // Handle
                          Positioned(
                            top: 10,
                            left: 0,
                            right: 0,
                            child: Center(
                              child: Container(
                                width: 40,
                                height: 5,
                                decoration: BoxDecoration(
                                  color: Colors.white.withOpacity(0.7),
                                  borderRadius: BorderRadius.circular(10),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                      
                      // Chef info
                      Container(
                        padding: const EdgeInsets.only(left: 20, right: 20, top: 60, bottom: 20),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      chef['name'],
                                      style: const TextStyle(
                                        fontSize: 24,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    const SizedBox(height: 4),
                                    Row(
                                      children: [
                                        RatingBar.builder(
                                          initialRating: chef['rating'],
                                          minRating: 1,
                                          direction: Axis.horizontal,
                                          allowHalfRating: true,
                                          itemCount: 5,
                                          itemSize: 18,
                                          ignoreGestures: true,
                                          itemBuilder: (context, _) => const Icon(
                                            Icons.star,
                                            color: Colors.amber,
                                          ),
                                          onRatingUpdate: (rating) {},
                                        ),
                                        const SizedBox(width: 8),
                                        Text(
                                          '${chef['rating']}',
                                          style: const TextStyle(
                                            fontSize: 16,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                                  decoration: BoxDecoration(
                                    color: const Color.fromARGB(255, 62, 113, 93).withOpacity(0.1),
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                ),
                              ],
                            ),
                            
                            const SizedBox(height: 16),
                            
                            // Speciality and experience
                            Row(
                              children: [
                                Expanded(
                                  child: _infoCard(
                                    icon: Icons.restaurant,
                                    title: 'Community',
                                    value: chef['speciality'],
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: _infoCard(
                                    icon: Icons.work,
                                    title: 'Experience',
                                    value: chef['experience'],
                                  ),
                                ),
                              ],
                            ),
                            
                            const SizedBox(height: 24),
                            
                            // About section
                            const Text(
                              'About',
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              chef['bio'],
                              style: TextStyle(
                                fontSize: 15,
                                color: Colors.grey[700],
                                height: 1.5,
                              ),
                            ),
                            
                            const SizedBox(height: 24),
                            
                            // Languages
                            const Text(
                              'Languages',
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 12),
                            Wrap(
                              spacing: 8,
                              runSpacing: 8,
                              children: chef['languages'].map<Widget>((language) {
                                return Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                  decoration: BoxDecoration(
                                    color: Colors.grey[100],
                                    borderRadius: BorderRadius.circular(16),
                                    border: Border.all(
                                      color: Colors.grey[300]!,
                                    ),
                                  ),
                                  child: Text(
                                    language,
                                    style: TextStyle(
                                      color: Colors.grey[800],
                                    ),
                                  ),
                                );
                              }).toList(),
                            ),
                            
                            const SizedBox(height: 24),
                            
                            // Availability
                            const Text(
                              'Availability',
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 12),
                            Container(
                              padding: const EdgeInsets.all(16),
                              decoration: BoxDecoration(
                                color: Colors.grey[50],
                                borderRadius: BorderRadius.circular(12),
                                border: Border.all(
                                  color: Colors.grey[200]!,
                                ),
                              ),
                              child: Column(
                                children: [
                                  Row(
                                    children: [
                                      const Icon(
                                        Icons.calendar_today,
                                        size: 16,
                                        color: Color.fromARGB(255, 62, 113, 93),
                                      ),
                                      const SizedBox(width: 8),
                                      Text(
                                        'Available from ${DateFormat('MMM d, yyyy').format(_startDate)}',
                                        style: const TextStyle(
                                          fontWeight: FontWeight.w500,
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 8),
                                  Row(
                                    children: [
                                      const Icon(
                                        Icons.access_time,
                                        size: 16,
                                        color: Color.fromARGB(255, 62, 113, 93),
                                      ),
                                      const SizedBox(width: 8),
                                      const Text(
                                        'Flexible hours',
                                        style: TextStyle(
                                          fontWeight: FontWeight.w500,
                                        ),
                                      ),
                                    ],
                                  ),
                                  if (_showPeakHours && chef['id'] % 3 == 0) ...[
                                    const SizedBox(height: 12),
                                    Container(
                                      padding: const EdgeInsets.all(12),
                                      decoration: BoxDecoration(
                                        color: Colors.amber[50],
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(color: Colors.amber[100]!),
                                      ),
                                      child: Row(
                                        children: [
                                          Icon(
                                            Icons.warning_amber_rounded,
                                            color: Colors.amber[700],
                                            size: 18,
                                          ),
                                          const SizedBox(width: 8),
                                          Expanded(
                                            child: Text(
                                              'Peak hour surcharge applies during 6-9 PM on weekdays',
                                              style: TextStyle(
                                                fontSize: 14,
                                                color: Colors.amber[900],
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ],
                              ),
                            ),
                            
                            const SizedBox(height: 80), // Space for booking button
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                
                // Floating booking button
                Positioned(
                  bottom: 20,
                  left: 20,
                  right: 20,
                  child: ElevatedButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => ChefBookingSummaryPage()),
    );
  },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color.fromARGB(255, 62, 113, 93),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      elevation: 4,
                    ),
                    child: const Text(
                      'Book This Chef',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
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
  
  Widget _infoCard({required IconData icon, required String title, required String value}) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                icon,
                size: 16,
                color: Colors.grey[600],
              ),
              const SizedBox(width: 4),
              Text(
                title,
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            value,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }
}

class PreferencesDialog extends StatefulWidget {
  final Function(DateTime, String, String, String, bool) onSubmit;

  const PreferencesDialog({Key? key, required this.onSubmit}) : super(key: key);

  @override
  _PreferencesDialogState createState() => _PreferencesDialogState();
}

class _PreferencesDialogState extends State<PreferencesDialog> {
  late DateTime _selectedDate;
  String _selectedGender = 'female';
  String _selectedTime = 'any';
  String _selectedCommunity = 'any';
  bool _showPeakHours = false;

  @override
  void initState() {
    super.initState();
    _selectedDate = DateTime.now().add(const Duration(days: 1));
  }

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime.now().add(const Duration(days: 1)),
      lastDate: DateTime(DateTime.now().year + 1),
      builder: (BuildContext context, Widget? child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.light(
              primary: Color.fromARGB(255, 62, 113, 93),
              onPrimary: Colors.white,
              onSurface: Colors.black,
            ),
            textButtonTheme: TextButtonThemeData(
              style: TextButton.styleFrom(
                foregroundColor: const Color.fromARGB(255, 62, 113, 93), // button text color
              ),
            ),
          ),
          child: child!,
        );
      },
    );
    if (picked != null && picked != _selectedDate) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Filter Chef Preferences'),
      content: SizedBox( // set width of the alert dialog
        width: MediaQuery.of(context).size.width * 1.0,
        height: MediaQuery.of(context).size.height*0.7,
        child: 
        SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Date selection
            const Text('Select Date:', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            InkWell(
              onTap: () => _selectDate(context),
              child: InputDecorator(
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.calendar_today, color: Color.fromARGB(255, 62, 113, 93)),
                ),
                child: Text(
                  DateFormat('MMM d, yyyy').format(_selectedDate),
                  style: const TextStyle(fontSize: 16),
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Gender preference
            const Text('Gender Preference:', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            DropdownButtonFormField<String>(
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.person, color: Color.fromARGB(255, 62, 113, 93)),
              ),
              value: _selectedGender,
              items: <String>['any', 'male', 'female']
                  .map((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value[0].toUpperCase() + value.substring(1)),
                );
              }).toList(),
              onChanged: (String? newValue) {
                setState(() {
                  _selectedGender = newValue!;
                });
              },
            ),
            const SizedBox(height: 16),

            // Time preference
            const Text('Time Preference:', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            DropdownButtonFormField<String>(
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.access_time, color: Color.fromARGB(255, 62, 113, 93)),
              ),
              value: _selectedTime,
              items: <String>['any', '6:00 am','7:00 am', '8:00 am', '9:00 am','10:00 am','11:00 am','12:00 am','1:00 pm','2:00 pm','3:00 pm','4:00 pm','5:00 pm','6:00 pm','7:00 pm','8:00 pm','9:00 pm','10:00 pm','11:00 pm','12:00 pm','1:00 am','2:00 am','3:00 am','4:00 am','5:00 am']
                  .map((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value[0].toUpperCase() + value.substring(1)),
                );
              }).toList(),
              onChanged: (String? newValue) {
                setState(() {
                  _selectedTime = newValue!;
                });
              },
            ),
            const SizedBox(height: 16),
            
          ],
        ),
      )),
      actions: <Widget>[
        TextButton(
          child: const Text('Cancel', style: TextStyle(color: Colors.grey)),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
        ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color.fromARGB(255, 62, 113, 93),
            foregroundColor: Colors.white,
          ),
          onPressed: () {
            widget.onSubmit(
              _selectedDate,
              _selectedGender,
              _selectedTime,
              _selectedCommunity,
              _showPeakHours,
            );
            Navigator.of(context).pop();
          },
          child: const Text('Apply Filters'),
        ),
      ],
    );
  }
}
//