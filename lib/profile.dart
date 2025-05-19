import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart'; // For SVG icons
import 'package:google_fonts/google_fonts.dart'; // For custom fonts

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Meri Didi App',
      theme: ThemeData(
        primarySwatch: Colors.orange, // Using orange as the primary color
        fontFamily:
            GoogleFonts.lato().fontFamily, // Using Lato as the primary font
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontSize: 16.0),
          bodyMedium: TextStyle(fontSize: 14.0),
          bodySmall: TextStyle(fontSize: 12.0),
          displayLarge: TextStyle(fontSize: 72.0, fontWeight: FontWeight.bold),
          displayMedium: TextStyle(fontSize: 56.0, fontWeight: FontWeight.bold),
          displaySmall: TextStyle(fontSize: 40.0),
          headlineLarge: TextStyle(fontSize: 32.0, fontWeight: FontWeight.bold),
          headlineMedium: TextStyle(fontSize: 28.0, fontWeight: FontWeight.bold),
          headlineSmall: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold),
          labelLarge: TextStyle(
              fontSize: 14.0, fontWeight: FontWeight.bold), // For button labels
          labelMedium: TextStyle(fontSize: 12.0, fontWeight: FontWeight.bold),
          labelSmall: TextStyle(fontSize: 11.0, fontWeight: FontWeight.bold),
        ),
        colorScheme:
            ColorScheme.fromSwatch().copyWith(secondary: Colors.orangeAccent),
      ),
      home: const AccountPage(),
    );
  }
}

class AccountPage extends StatelessWidget {
  const AccountPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor:
          Colors.white, // Setting the background color of the entire page
      appBar: AppBar(
        backgroundColor: Colors.white, // Appbar background white
        elevation: 0, // Removing shadow
        leading: IconButton(
          icon: const Icon(Icons.arrow_back,
              color: Colors.black), // Black back arrow
          onPressed: () {
            // Handle back button press
          },
        ),
        title: const Text(
          'Account', // Keeping the title as 'Account'
          style: TextStyle(color: Colors.black), // Making title black
        ),
        centerTitle: true, // Center aligning the title
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              _buildProfileSection(context), // Extracting profile section
              const SizedBox(height: 24), // Increased spacing
              _buildOptionCard(
                context,
                title: 'My Bookings',
                icon: 'assets/icons/bookings.svg', // Placeholder SVG
              ),
              const SizedBox(height: 16),
              _buildOptionCard(
                context,
                title: 'Wallet',
                icon: 'assets/icons/wallet.svg', // Placeholder SVG
              ),
              const SizedBox(height: 24), // Increased spacing
              _buildListTile(context,
                  title: 'My Plans', icon: Icons.card_membership),
              _buildListTile(context,
                  title: 'Plus Membership', icon: Icons.star_border),
              _buildListTile(context,
                  title: 'My Ratings', icon: Icons.star_half),
              _buildListTile(context,
                  title: 'Manage addresses', icon: Icons.location_on_outlined),
              _buildListTile(context,
                  title: 'Manage payment methods',
                  icon: Icons.payment_outlined),
              _buildListTile(context, title: 'Settings', icon: Icons.settings),
              const SizedBox(height: 24), // Increased spacing
              _buildListTile(context,
                  title: 'About Meri Didi', icon: Icons.info_outline),
              _buildListTile(context,
                  title: 'Report worker', icon: Icons.report_problem_outlined),
              _buildListTile(context,
                  title: 'Log out', icon: Icons.logout), // Using logout icon
              const SizedBox(height: 32), // Increased spacing
              const Center(
                child: Text(
                  'Version 1.0.01', // Moved version to the bottom
                  style: TextStyle(color: Colors.grey),
                ),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: _buildBottomNavigationBar(context),
    );
  }

  // Method for building the profile section
  Widget _buildProfileSection(BuildContext context) {
    return Row(
      children: <Widget>[
        const CircleAvatar(
          radius: 40,
          backgroundImage:
              NetworkImage('https://via.placeholder.com/80'), // Placeholder image
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Text(
                'Shantanu Sontakke',
                style: Theme.of(context).textTheme.headlineSmall,
              ),
              Text(
                'shantanu@gmail.com',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: Colors.grey,
                    ),
              ),
              Text(
                '+91 98865 76685',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: Colors.grey,
                    ),
              ),
            ],
          ),
        ),
        IconButton(
          icon: const Icon(Icons.edit_outlined), // Using edit icon
          onPressed: () {
            // Handle edit profile
          },
        ),
      ],
    );
  }

  // Method for building the rectangular option cards
  Widget _buildOptionCard(BuildContext context,
      {required String title, required String icon}) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
        color: const Color(0xFFFFF3E0), // Light orange background,
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: <Widget>[
            SvgPicture.asset(
              icon,
              width: 24, // Adjusted icon size
              height: 24,
              color: Colors.orange, // Made icon color orange
            ),
            const SizedBox(width: 16),
            Text(
              title,
              style: Theme.of(context)
                  .textTheme
                  .headlineSmall
                  ?.copyWith(fontWeight: FontWeight.w500), // Semi-bold
            ),
          ],
        ),
      ),
    );
  }

  // Method for building the list tile options
  Widget _buildListTile(BuildContext context,
      {required String title, required IconData icon}) {
    return ListTile(
      leading: Icon(
        icon,
        color: Colors.orange, // Made icon color orange
      ),
      title: Text
        (title, style: Theme.of(context).textTheme.bodyLarge), //Using bodyLarge
      trailing:
          const Icon(Icons.chevron_right, color: Colors.grey), // Arrow icon
      onTap: () {
        // Handle tile tap
      },
    );
  }

  // Method for bottom navigation bar
  Widget _buildBottomNavigationBar(BuildContext context) {
    return BottomNavigationBar(
      type: BottomNavigationBarType.fixed, // Fixed bottom nav bar
      backgroundColor: Colors.white, // White background
      selectedItemColor: Colors.orange, // Orange for selected item
      unselectedItemColor: Colors.grey, // Grey for unselected item
      showSelectedLabels: true, // Show labels for selected items
      showUnselectedLabels:
          true, // Show labels for unselected items - set to true
      items: const <BottomNavigationBarItem>[
        BottomNavigationBarItem(
          icon: Icon(Icons.home_outlined), // Home icon
          label: 'Home',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.cleaning_services_outlined), // Services icon
          label: 'Services',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.book_outlined), // Bookings icon
          label: 'Bookings',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.person_outline), // Account icon
          label: 'Account',
        ),
      ],
      currentIndex: 3, // Index for the Account page
      onTap: (int index) {
        // Handle bottom navigation item tap
        if (index == 0) {
          // Navigate to Home
        } else if (index == 1) {
          // Navigate to Services
        } else if (index == 2) {
          // Navigate to Bookings
        } else if (index == 3) {
          // Navigate to Account (Current Page)
        }
      },
    );
  }
}
