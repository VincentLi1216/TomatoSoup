package com.delicious.tomatosoup.ui.folder

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.delicious.tomatosoup.adapter.CourseAdapter
import com.delicious.tomatosoup.databinding.FragmentCourseBinding
import com.google.android.material.snackbar.Snackbar
import com.google.firebase.firestore.DocumentSnapshot
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.FirebaseFirestoreException
import com.google.firebase.firestore.Query
import com.google.firebase.firestore.ktx.firestore
import com.google.firebase.ktx.Firebase

/**
 * A simple [Fragment] subclass as the second destination in the navigation.
 */
open class CourseFragment : Fragment(),
    CourseAdapter.onCourseSelectedListener {

    lateinit var db: FirebaseFirestore
    private var query: Query? = null

    private var _binding: FragmentCourseBinding? = null
    private val binding get() = _binding!!

    private var adapter: CourseAdapter? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentCourseBinding.inflate(inflater, container, false)
        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        db = Firebase.firestore
        query = db.collection("sorted_by_subject")

        query?.let {
            adapter = object : CourseAdapter(it, this@CourseFragment) {
                override fun onDataChanged() {
                    // Show/hide content if the query returns empty.
                    if (itemCount == 0) {
//                        binding.recyclerCourse.visibility = View.GONE
//                        binding.viewEmpty.visibility = View.VISIBLE
                    } else {
                        binding.recyclerCourse.visibility = View.VISIBLE
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
            binding.recyclerCourse.adapter = adapter
        }

        binding.recyclerCourse.layoutManager = LinearLayoutManager(context)

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

    override fun onCourseSelected(course: DocumentSnapshot) {

        val action = CourseFragmentDirections.actionCourseFragmentToDateFragment(course.id)
        findNavController().navigate(action)
    }
}