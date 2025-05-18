import 'package:flutter/material.dart';
import 'package:home_ease/getstarted.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Supabase.initialize(
    url: 'https://hhginjabqhgalovkvboe.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhoZ2luamFicWhnYWxvdmt2Ym9lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcyMzI2NzEsImV4cCI6MjA2MjgwODY3MX0.kVOdl_qGtEVLUCB6yc9yucuZp-qTl5GZIk5ywxCin2c',
  );

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Home Services',
      theme: ThemeData(
        fontFamily: 'Helvetica',
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: Colors.white,
      ),
      home: const HomeServicesScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomeServicesScreen extends StatefulWidget {
  const HomeServicesScreen({Key? key}) : super(key: key);

  @override
  State<HomeServicesScreen> createState() => _HomeServicesScreenState();
}

class _HomeServicesScreenState extends State<HomeServicesScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  final List<String> _images = [
    'assets/chef/cookin.jpg',
    'assets/chef/dusting.jpg',
    'assets/chef/acrepair.png',
    'assets/chef/carwash.jpg',
  ];

  @override
  void initState() {
    super.initState();
    _pageController.addListener(() {
      int next = _pageController.page!.round();
      if (_currentPage != next) {
        setState(() {
          _currentPage = next;
        });
      }
    });
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // Image Carousel
          Expanded(
            child: PageView.builder(
              controller: _pageController,
              itemCount: _images.length,
              itemBuilder: (context, index) {
                return Container(
                  width: MediaQuery.of(context).size.width,
                  color: Colors.black,
                  child: Image.asset(
                    _images[index],
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) {
                      // If image fails to load, show cooking image similar to screenshot
                      return Image.asset('assets/chef/cookin.jpg',
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) {
                          return Container(
                            color: Colors.black87,
                            child: Center(
                              child: Icon(
                                Icons.restaurant,
                                size: 50,
                                color: Colors.grey.shade300,
                              ),
                            ),
                          );
                        },
                      );
                    },
                  ),
                );
              },
            ),
          ),
          
          // Bottom section with text and button - matches the cream color in the screenshot
          Container(
            padding: const EdgeInsets.all(24),
            color: const Color(0xFFF8F5E7), // Cream color from screenshot
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Title text
                const Text(
                  'Making Home\nServices Effortless.',
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF2D3B2D), // Dark green color from screenshot
                    height: 1.2,
                  ),
                ),
                const SizedBox(height: 12),
                
                // Description text
                Text(
                  'Book trusted professionals at your\ndoorstep, anytime.',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.grey.shade700,
                    height: 1.4,
                  ),
                ),
                const SizedBox(height: 28),
                
                // Page indicators
                Row(
                  children: [
                    for (int i = 0; i < _images.length; i++)
                      Container(
                        margin: const EdgeInsets.only(right: 6),
                        width: 8,
                        height: 8,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: _currentPage == i
                              ? const Color(0xFF2D3B2D) // Dark green for active
                              : Colors.grey.shade300, // Light grey for inactive
                        ),
                      ),
                    const Spacer(),
                  ],
                ),
                const SizedBox(height: 24),
                
                // Get Started button
                Center(
                  child: ElevatedButton(
                    onPressed: () {
                      Navigator.push(context, MaterialPageRoute(builder: (context) => SignUpScreen()));
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFF6FF00), // Bright yellow from screenshot
                      foregroundColor: Colors.black,
                      padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                      ),
                      elevation: 0,
                      minimumSize: const Size(220, 50),
                    ),
                    child: const Text(
                      'Get Started',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.black,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}