import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:home_ease/booking_summary.dart';
import 'package:intl/intl.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

class ChefProfilesPage extends StatefulWidget {
  final double totalPrice;
  
  const ChefProfilesPage({
    Key? key,
    required this.totalPrice,
  }) : super(key: key);

  @override
  _ChefProfilesPageState createState() => _ChefProfilesPageState();
}

class _ChefProfilesPageState extends State<ChefProfilesPage>
    with SingleTickerProviderStateMixin {
  DateTime _startDate = DateTime.now().add(const Duration(days: 1));
  String _genderPreference = 'female';
  String _timePreference = 'any';
  String _communityPreference = 'any';
  TimeOfDay _selectedTime = TimeOfDay(hour: 12, minute: 0);
  double _currentTotalPrice = 0.0;

  late AnimationController _animationController;
  List<Map<String, dynamic>> _chefs = [];
  bool _isLoading = false;
  int _currentPage = 0;

  @override
  void initState() {
    super.initState();
    _currentTotalPrice = widget.totalPrice;
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );

    WidgetsBinding.instance.addPostFrameCallback((_) {
      _showPreferencesDialog();
    });

    _loadChefs();
  }

  Future<void> _loadChefs() async {
    if (_isLoading) return;

    setState(() {
      _isLoading = true;
    });

    try {
      var query = Supabase.instance.client.from('chef').select();

      if (_genderPreference != 'any') {
        query = query.eq('gender', _genderPreference);
      }
      if (_communityPreference != 'any') {
        query = query.eq('community', _communityPreference);
      }

      final List<dynamic> data =
          await query.range(_currentPage * 8, _currentPage * 8 + 7);

      setState(() {
        _chefs.addAll(data.map((chef) {
          return {
            'id': chef['id'],
            'name': chef['name'],
            'image': chef['image'],
            'rating': chef['rating'] ?? 0.0,
            'experience': chef['experience'] ?? '',
            'bio': chef['bio'] ?? '',
            'languages': chef['languages'] != null
                ? (chef['languages'] is String
                    ? chef['languages'].split(',').map((e) => e.trim()).toList()
                    : List<String>.from(chef['languages']))
                : <String>[],
            'community': chef['community'] ?? '',
            'speciality': chef['speciality'] ?? chef['community'] ?? '',
            'gender': chef['gender'] ?? '',
          };
        }).toList());
        _currentPage++;
      });
    } catch (e) {
      print('Exception fetching chefs: $e');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
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
        initialStartDate: _startDate,
        initialGender: _genderPreference,
        initialTime: _timePreference,
        initialCommunity: _communityPreference,
        onSubmit: (startDate, gender, timePreference, community, selectedTime) {
          setState(() {
            _startDate = startDate;
            _genderPreference = gender;
            _timePreference = timePreference;
            _communityPreference = community;
            _selectedTime = selectedTime;
            _chefs = [];
            _currentPage = 0;
          });
          _loadChefs();
        },
      ),
    );
  }

  void _navigateToBookingSummary(Map<String, dynamic> chef) {
    // Add community surcharge if applicable
    double finalPrice = _currentTotalPrice;
    if (chef['community'] != null && chef['community'].toString().toLowerCase() != 'Any') {
      finalPrice += 1000.0;
    }

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ChefBookingSummaryPage(
          chef: chef,
          startDate: _startDate,
          selectedTime: _selectedTime,
          totalPrice: finalPrice,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFEF54A).withOpacity(0.15),
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
            icon: const Icon(Icons.tune, color: Color(0xFF2E3C59)),
            onPressed: _showPreferencesDialog,
            tooltip: 'Chef Preferences',
          ),
        ],
      ),
      body: Column(
        children: [
          if (_genderPreference != 'any' ||
              _timePreference != 'any' ||
              _communityPreference != 'any')
            Container(
              padding:
                  const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              color: const Color(0xFFFEF54A).withOpacity(0.06),
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [
                    _filterChip(
                      label:
                          'Date: ${DateFormat('MMM d, yyyy').format(_startDate)}',
                      icon: Icons.calendar_today,
                    ),
                    _filterChip(
                      label: 'Time: ${_selectedTime.format(context)}',
                      icon: Icons.access_time,
                    ),
                    if (_genderPreference != 'any')
                      _filterChip(
                        label:
                            'Gender: ${_genderPreference[0].toUpperCase() + _genderPreference.substring(1)}',
                        icon: _genderPreference == 'male'
                            ? Icons.male
                            : Icons.female,
                      ),
                    if (_communityPreference != 'any')
                      _filterChip(
                        label:
                            'Community: ${_communityPreference[0].toUpperCase() + _communityPreference.substring(1)}',
                        icon: Icons.groups,
                      ),
                  ],
                ),
              ),
            ),
          Expanded(
            child: LayoutBuilder(
              builder: (context, constraints) {
                final double width = constraints.maxWidth;
                int crossAxisCount = 2;
                if (width > 600) crossAxisCount = 3;
                if (width > 900) crossAxisCount = 4;

                return RefreshIndicator(
                  onRefresh: () async {
                    setState(() {
                      _chefs = [];
                      _currentPage = 0;
                    });
                    await _loadChefs();
                  },
                  color: const Color.fromARGB(255, 62, 113, 93),
                  child: CustomScrollView(
                    physics: const AlwaysScrollableScrollPhysics(),
                    slivers: [
                      SliverPadding(
                        padding: const EdgeInsets.all(16),
                        sliver: SliverGrid(
                          gridDelegate:
                              SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: crossAxisCount,
                            childAspectRatio: 0.75,
                            crossAxisSpacing: 16,
                            mainAxisSpacing: 16,
                          ),
                          delegate: SliverChildBuilderDelegate(
                            (context, index) {
                              if (index >= _chefs.length) return null;

                              final chef = _chefs[index];
                              return AnimatedBuilder(
                                animation: _animationController,
                                builder: (context, child) {
                                  final delay =
                                      index % (crossAxisCount * 2) * 0.1;
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
                                  valueColor: AlwaysStoppedAnimation<Color>(
                                      Color.fromARGB(255, 62, 113, 93)),
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

  Widget _filterChip(
      {required String label, required IconData icon, Color? color}) {
    return Container(
      margin: const EdgeInsets.only(right: 8),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color ?? const Color(0xFFEDF7ED),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: color != null
              ? color.withOpacity(0.3)
              : const Color(0xFF2E3C59).withOpacity(0.3),
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            size: 16,
            color: color ?? const Color(0xFF2E3C59),
          ),
          const SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              color: color ?? const Color(0xFF2E3C59),
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildChefCard(Map<String, dynamic> chef) {
    return GestureDetector(
      onTap: () => _navigateToBookingSummary(chef),
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
            Expanded(
              flex: 5,
              child: Container(
                decoration: BoxDecoration(
                  borderRadius:
                      const BorderRadius.vertical(top: Radius.circular(16)),
                  image: DecorationImage(
                    image: NetworkImage(chef['image']),
                    fit: BoxFit.cover,
                  ),
                ),
              ),
            ),
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
                    Row(
                      children: [
                        RatingBar.builder(
                          initialRating: (chef['rating'] as num).toDouble(),
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

  // --- UPDATED CHEF DETAILS MODAL WITH CIRCLEAVATAR AND YELLOW BG ---
  void _showChefDetails(Map<String, dynamic> chef) {
    bool _showPeakHours = true;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => Stack(
        children: [
          Container(
            margin: const EdgeInsets.only(top: 60),
            decoration: const BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
            ),
            child: SingleChildScrollView(
              padding: const EdgeInsets.only(
                  left: 20, right: 20, top: 60, bottom: 20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Name, rating, badge
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
                                initialRating:
                                    (chef['rating'] as num).toDouble(),
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
                        padding: const EdgeInsets.symmetric(
                            horizontal: 12, vertical: 8),
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 62, 113, 93)
                              .withOpacity(0.1),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          chef['speciality'] ?? chef['community'] ?? '',
                          style: const TextStyle(
                            color: Color.fromARGB(255, 62, 113, 93),
                            fontWeight: FontWeight.bold,
                          ),
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
                          icon: Icons.groups,
                          title: 'Community',
                          value: chef['speciality'] ?? chef['community'] ?? '',
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
                    children: (chef['languages'] as List)
                        .map<Widget>((language) {
                      return Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 12, vertical: 6),
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
                              color: Color(0xFF2E3C59),
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
                              color: Color(0xFF2E3C59),
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
                        
                      ],
                    ),
                  ),

                  const SizedBox(height: 80),
                ],
              ),
            ),
          ),
          // Chef Image in CircleAvatar with yellow background, floating above modal
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: Center(
              child: Container(
                width: 110,
                height: 110,
                decoration: const BoxDecoration(
                  color: Color(0xFFFEF54A),
                  shape: BoxShape.circle,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black12,
                      blurRadius: 10,
                      offset: Offset(0, 4),
                    ),
                  ],
                ),
                child: CircleAvatar(
                  radius: 52,
                  backgroundColor: Colors.transparent,
                  backgroundImage: NetworkImage(chef['image']),
                ),
              ),
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
                  MaterialPageRoute(
                    builder: (context) => ChefBookingSummaryPage(
                      chef: chef,
                      startDate: _startDate,
                      selectedTime: _selectedTime,
                      totalPrice: _currentTotalPrice + (chef['community'] != null && 
                        chef['community'].toString().toLowerCase() != 'any' ? 1000.0 : 0.0),
                    ),
                  ),
                );
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFFFEF54A),
                foregroundColor: const Color(0xFF2E3C59),
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
  }

  Widget _infoCard(
      {required IconData icon, required String title, required String value}) {
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
                style: const TextStyle(
                  fontSize: 12,
                  color: Colors.grey,
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

// Dummy Booking Summary Page (replace with real one)


// PreferencesDialog with original (white) colors
class PreferencesDialog extends StatefulWidget {
  final DateTime initialStartDate;
  final String initialGender;
  final String initialTime;
  final String initialCommunity;
  final void Function(DateTime, String, String, String, TimeOfDay) onSubmit;

  const PreferencesDialog({
    Key? key,
    required this.initialStartDate,
    required this.initialGender,
    required this.initialTime,
    required this.initialCommunity,
    required this.onSubmit,
  }) : super(key: key);

  @override
  State<PreferencesDialog> createState() => _PreferencesDialogState();
}

class _PreferencesDialogState extends State<PreferencesDialog> {
  late DateTime _startDate;
  late String _gender;
  late String _time;
  late String _community;
  late TimeOfDay _selectedTime;

  final List<String> _genders = ['any', 'male', 'female'];
  final List<String> _communities = [
    'any',
    'jain',
    'marwadi',
    'hindu',
    'muslim',
    'parsi',
    'christian',
    'buddhist'
  ];

  @override
  void initState() {
    super.initState();
    _startDate = widget.initialStartDate;
    _gender = widget.initialGender;
    _time = widget.initialTime;
    _community = widget.initialCommunity;
    _selectedTime = TimeOfDay(hour: 12, minute: 0); // Default time
  }

  void _showDatePicker() {
    showDialog(
      context: context,
      builder: (context) {
        DateTime tempPickedDate = _startDate;
        return AlertDialog(
          title: const Text('Select Date'),
          content: SizedBox(
            height: 180,
            child: CupertinoDatePicker(
              mode: CupertinoDatePickerMode.date,
              initialDateTime: _startDate,
              minimumDate: DateTime.now(),
              maximumDate: DateTime.now().add(const Duration(days: 365)),
              onDateTimeChanged: (newDate) {
                tempPickedDate = newDate;
              },
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                setState(() {
                  _startDate = tempPickedDate;
                });
                Navigator.of(context).pop();
              },
              child: const Text('Select'),
            ),
          ],
        );
      },
    );
  }

  void _showTimePicker() {
    showDialog(
      context: context,
      builder: (context) {
        TimeOfDay tempPickedTime = _selectedTime;
        return AlertDialog(
          title: const Text('Select Time'),
          content: SizedBox(
            height: 180,
            child: CupertinoDatePicker(
              mode: CupertinoDatePickerMode.time,
              initialDateTime: DateTime(
                0,
                0,
                0,
                _selectedTime.hour,
                _selectedTime.minute,
              ),
              use24hFormat: false,
              onDateTimeChanged: (newTime) {
                tempPickedTime = TimeOfDay(hour: newTime.hour, minute: newTime.minute);
              },
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                setState(() {
                  _selectedTime = tempPickedTime;
                });
                Navigator.of(context).pop();
              },
              child: const Text('Select'),
            ),
          ],
        );
      },
    );
  }

  @override
Widget build(BuildContext context) {
  return Dialog(
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(20),
    ),
    backgroundColor: Colors.white, // So inner containers control color
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Header (Dark Yellow)
        Container(
          width: double.infinity,
          decoration: BoxDecoration(
            color: Color(0xFFFEF54A), // Dark Yellow
            borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
          ),
          padding: const EdgeInsets.all(16),
          child: const Center(
            child: Text(
              'Chef Preferences',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
          ),
        ),

        // Body (Light Yellow)
        Container(
          decoration: BoxDecoration(
            color: const Color(0xFFFEF54A).withOpacity(0.15), // Light Yellow
            borderRadius: BorderRadius.vertical(bottom: Radius.circular(20)),
          ),
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Date picker
                ListTile(
                  leading: const Icon(Icons.calendar_today),
                  title: Text('Start Date: ${DateFormat('MMM d, yyyy').format(_startDate)}'),
                  trailing: IconButton(
                    icon: const Icon(Icons.edit),
                    onPressed: () {
                      _showDatePicker();
                    },
                  ),
                ),

                // Time picker
                ListTile(
                  leading: const Icon(Icons.access_time),
                  title: Text('Time: ${_selectedTime.format(context)}'),
                  trailing: IconButton(
                    icon: const Icon(Icons.edit),
                    onPressed: () {
                      _showTimePicker();
                    },
                  ),
                ),

                // Gender dropdown
                ListTile(
                  leading: const Icon(Icons.person),
                  title: const Text('Gender'),
                  trailing: DropdownButton<String>(
                    value: _gender,
                    items: _genders
                        .map((g) => DropdownMenuItem(
                              value: g,
                              child: Text(g[0].toUpperCase() + g.substring(1)),
                            ))
                        .toList(),
                    onChanged: (val) {
                      if (val != null) setState(() => _gender = val);
                    },
                  ),
                ),

                // Community dropdown
                ListTile(
                  leading: const Icon(Icons.groups),
                  title: const Text('Community'),
                  trailing: DropdownButton<String>(
                    value: _community,
                    items: _communities
                        .map((c) => DropdownMenuItem(
                              value: c,
                              child: Text(c[0].toUpperCase() + c.substring(1)),
                            ))
                        .toList(),
                    onChanged: (val) {
                      if (val != null) setState(() => _community = val);
                    },
                  ),
                ),

                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    TextButton(
                      child: const Text('Cancel',style: TextStyle(color: Colors.black),),
                      onPressed: () => Navigator.of(context).pop(),
                    ),
                    const SizedBox(width: 8),
                    ElevatedButton(
                      child: const Text('Apply'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFFEF54A),
                        foregroundColor: Colors.black,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                      ),
                      onPressed: () {
                        widget.onSubmit(
                            _startDate, _gender, _time, _community, _selectedTime);
                        Navigator.of(context).pop();
                      },
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ],
    ),
  );
}
}