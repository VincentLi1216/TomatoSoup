package com.delicious.tomatosoup.ui

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.navigateUp
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.delicious.tomatosoup.R
import com.delicious.tomatosoup.databinding.ActivityMainBinding
import com.firebase.ui.auth.AuthUI
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser

class MainActivity : AppCompatActivity() {

    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityMainBinding
    private lateinit var firebaseAuth: FirebaseAuth
    private lateinit var listener: FirebaseAuth.IdTokenListener

    override fun onCreate(savedInstanceState: Bundle?) {
        WindowCompat.setDecorFitsSystemWindows(window, false)
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setSupportActionBar(binding.toolbar)

        val bottomNavigation = binding.bottomNavigation

        val navController = findNavController(R.id.nav_host_fragment)
        appBarConfiguration = AppBarConfiguration(
            setOf(
                R.id.CourseFragment, R.id.HomeFragment, R.id.ProfileFragment
            )
        )

        setupActionBarWithNavController(navController, appBarConfiguration)
        bottomNavigation.setupWithNavController(navController)

        firebaseAuth = FirebaseAuth.getInstance()
        listener = FirebaseAuth.IdTokenListener {
            val user = it.currentUser
            if (user == null) {
                startActivity(Intent(this@MainActivity, LoginActivity::class.java))
                finish()
            }
        }

//        navController.addOnDestinationChangedListener { _, destination, _ ->
//            if(destination.id == R.id.ProfileFragment) {
//                val user = firebaseAuth.currentUser
//                binding.toolbar.title = user?.displayName
//            }
//        }


//        bottomNavigation.setOnItemSelectedListener {
//            when (it.itemId) {
//                R.id.ProfileFragment -> {
//                    binding.toolbar.title = user!!.displayName
//                    true
//                }
//                else -> true
//            }
//        }
    }

    override fun onStart() {
        super.onStart()
        firebaseAuth.addIdTokenListener(listener)
    }

    override fun onStop() {
        super.onStop()
        firebaseAuth.removeIdTokenListener(listener)
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_main, menu)
        return super.onCreateOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        when(item.itemId) {
            R.id.action_logout -> {
                AuthUI.getInstance().signOut(this).addOnCompleteListener {
                    if (it.isSuccessful) {
                        Toast.makeText(this, "Successfully Logged out !", Toast.LENGTH_SHORT).show()
                    }
                }
//                startActivity(Intent(this, FirebaseUIActivity::class.java))
            }
        }
        return super.onOptionsItemSelected(item)
    }

    override fun onSupportNavigateUp(): Boolean {
        val navController = findNavController(R.id.nav_host_fragment)
        return navController.navigateUp(appBarConfiguration)
                || super.onSupportNavigateUp()
    }
}