package com.delicious.tomatosoup.ui.folder

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import androidx.recyclerview.widget.LinearLayoutManager
import com.delicious.tomatosoup.adapter.DateAdapter
import com.delicious.tomatosoup.databinding.FragmentDateBinding
import com.google.android.material.snackbar.Snackbar
import com.google.firebase.firestore.*
import com.google.firebase.firestore.ktx.firestore
import com.google.firebase.ktx.Firebase

class DateFragment : Fragment(),
    DateAdapter.onDateSelectedListener {

    private lateinit var db: FirebaseFirestore
    private var query: Query? = null
    private lateinit var courseRef: DocumentReference

    private var _binding: FragmentDateBinding? = null
    private val binding get() = _binding!!

    private var adapter: DateAdapter? = null
    private val args: DateFragmentArgs by navArgs()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        // Inflate the layout for this fragment
        _binding = FragmentDateBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

//        className = DateFragmentArgs.fromBundle(requireArguments()).keyCourseId

        db = Firebase.firestore
        courseRef = db.collection("sorted_by_subject").document(args.keyCourseId)
        query = courseRef.collection("dates")

        query?.let {
            adapter = object : DateAdapter(it, this@DateFragment) {
                override fun onDataChanged() {
                    if (itemCount == 0) {
//                        binding.recyclerDate.visibility = View.GONE
//                        binding.viewEmpty.visibility = View.VISIBLE
                    } else {
                        binding.recyclerDate.visibility = View.VISIBLE
//                        binding.viewEmpty.visibility = View.GONE
                    }
                }

                override fun onError(e: FirebaseFirestoreException) {
                    // Show a snackbar on errors
                    Snackbar.make(
                        binding.root,
                        "Error: check logs for info.", Snackbar.LENGTH_LONG
                    ).show()
                }
            }
            binding.recyclerDate.adapter = adapter
        }

        binding.recyclerDate.layoutManager = LinearLayoutManager(context)
//        binding.recyclerDate.layoutManager = GridLayoutManager(context, 2)

    }

    override fun onStart() {
        super.onStart()
        adapter?.startListening()
    }

    override fun onStop() {
        super.onStop()
        adapter?.stopListening()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    override fun onDateSelected(date: DocumentSnapshot) {
        val action = DateFragmentDirections.actionDateFragmentToPictureFragment(date.id, args.keyCourseId)
        findNavController().navigate(action)
    }
}