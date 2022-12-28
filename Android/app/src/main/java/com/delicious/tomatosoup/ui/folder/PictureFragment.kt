package com.delicious.tomatosoup.ui.folder

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.fragment.navArgs
import androidx.recyclerview.widget.LinearLayoutManager
import com.delicious.tomatosoup.adapter.PictureAdapter
import com.delicious.tomatosoup.databinding.FragmentPictureBinding
import com.delicious.tomatosoup.ui.folder.viewmodel.PictureViewModel
import com.google.android.material.snackbar.Snackbar
import com.google.firebase.firestore.*
import com.google.firebase.firestore.ktx.firestore
import com.google.firebase.ktx.Firebase

class PictureFragment : Fragment(),
    PictureAdapter.onPictureSelectedListener {

    private lateinit var db: FirebaseFirestore
    private var query: Query? = null
    private lateinit var dateRef: DocumentReference

    private var _binding: FragmentPictureBinding? = null
    private val binding get() = _binding!!

    private lateinit var viewModel: PictureViewModel

    private var adapter: PictureAdapter? = null
    private val args: PictureFragmentArgs by navArgs()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentPictureBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        db = Firebase.firestore
        dateRef = db.collection("sorted_by_subject")
            .document(args.keyCourseId)
            .collection("dates")
            .document(args.keyDateId)
        query = dateRef.collection("pics")

        query?.let {
            adapter = object : PictureAdapter(it, this@PictureFragment) {
                override fun onDataChanged() {
                    if (itemCount == 0) {
//                        binding.recyclerPicture.visibility = View.GONE
//                        binding.viewEmpty.visibility = View.VISIBLE
                    } else {
                        binding.recyclerPicture.visibility = View.VISIBLE
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
            binding.recyclerPicture.adapter = adapter
        }
        binding.recyclerPicture.layoutManager = LinearLayoutManager(context)

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

    override fun onPictureSelected(date: DocumentSnapshot) {
        TODO("Not yet implemented")
    }
}