package com.example.phishguard

import android.content.ClipboardManager
import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity

import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.phishguard.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 1. Enable Full Screen (Edge-to-Edge)
        enableEdgeToEdge()

        // 2. Setup View Binding
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // 3. Handle System Bars (Status Bar / Nav Bar) so content isn't hidden
        ViewCompat.setOnApplyWindowInsetsListener(binding.root) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 4. Auto-Paste from Clipboard when app opens
        checkClipboard()

        // 5. Scan Button Listener
        binding.btnScan.setOnClickListener {
            val url = binding.etUrl.text.toString()
            if (url.isNotEmpty()) {
                startScanningAnimation(url)
            } else {
                Toast.makeText(this, "Please enter a URL", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun checkClipboard() {
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        // Check if clipboard has content
        if (clipboard.hasPrimaryClip()) {
            val clipData = clipboard.primaryClip
            val item = clipData?.getItemAt(0)
            val text = item?.text.toString()

            // Only paste if it looks like a link
            if (text.contains("http") || text.contains("www")) {
                binding.etUrl.setText(text)
                Toast.makeText(this, "Link pasted from clipboard", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun startScanningAnimation(url: String) {
        // UI: Show "Scanning..." state
        binding.btnScan.text = "SCANNING..."
        binding.btnScan.isEnabled = false
        binding.cvResult.visibility = View.GONE

        // Logic: Fake a 1.5 second network delay for effect
        Handler(Looper.getMainLooper()).postDelayed({
            analyzeLink(url)
            binding.btnScan.text = "INITIATE SCAN"
            binding.btnScan.isEnabled = true
        }, 1500)
    }

    private fun analyzeLink(url: String) {
        val lowerUrl = url.lowercase()
        var isPhishing = false
        var reason = ""

        // --- HACKATHON HEURISTIC LOGIC ---
        // Add more words here to make the demo smarter
        val suspiciousWords = listOf("free", "prize", "login", "bank", "verify", "ngrok", "secure-account", "update-now")

        if (suspiciousWords.any { lowerUrl.contains(it) }) {
            isPhishing = true
            reason = "Suspicious keywords detected (Social Engineering)."
        } else if (url.matches(Regex(".*\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}.*"))) {
            isPhishing = true
            reason = "Raw IP address usage detected (High Risk)."
        } else if (lowerUrl.startsWith("http://")) {
            isPhishing = true
            reason = "Unsecured connection (HTTP)."
        }

        showResult(isPhishing, reason)
    }

    private fun showResult(isPhishing: Boolean, reason: String) {
        binding.cvResult.visibility = View.VISIBLE

        if (isPhishing) {
            // DANGER UI (Red Theme)
            binding.tvResultTitle.text = "⚠️ THREAT DETECTED"
            binding.tvResultTitle.setTextColor(Color.parseColor("#FF0033"))
            binding.tvResultDesc.text = reason

            // Change Input Box & Icon to Red
            binding.tilInput.boxStrokeColor = Color.parseColor("#FF0033")
            binding.ivShield.setColorFilter(Color.parseColor("#FF0033"))
            binding.ivShield.setImageResource(android.R.drawable.ic_delete)

        } else {
            // SAFE UI (Green Theme)
            binding.tvResultTitle.text = "✅ LINK VERIFIED SAFE"
            binding.tvResultTitle.setTextColor(Color.parseColor("#00FF41"))
            binding.tvResultDesc.text = "No known threats found in local database."

            // Change Input Box & Icon to Green
            binding.tilInput.boxStrokeColor = Color.parseColor("#00FF41")
            binding.ivShield.setColorFilter(Color.parseColor("#00FF41"))
            binding.ivShield.setImageResource(android.R.drawable.ic_lock_idle_lock)
        }
    }
}