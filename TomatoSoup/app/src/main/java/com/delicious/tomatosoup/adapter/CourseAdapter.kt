package com.delicious.tomatosoup.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.delicious.tomatosoup.R
import com.delicious.tomatosoup.databinding.CourseItemBinding
import com.delicious.tomatosoup.model.Course
import com.google.android.material.snackbar.Snackbar
import com.google.android.material.snackbar.Snackbar.make
import com.google.firebase.firestore.DocumentSnapshot
import com.google.firebase.firestore.Query
import com.google.firebase.firestore.ktx.toObject

open class CourseAdapter(query: Query, private val listener: onCourseSelectedListener) :
    FirestoreAdapter<CourseAdapter.CourseViewHolder>(query){

    interface onCourseSelectedListener {
        fun onCourseSelected(course: DocumentSnapshot)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CourseViewHolder {
        return CourseViewHolder(CourseItemBinding.inflate(
            LayoutInflater.from(parent.context), parent, false))
    }

    override fun onBindViewHolder(holder: CourseViewHolder, position: Int) {
        holder.bind(getSnapshot(position), listener)
    }

    class CourseViewHolder(private val binding: CourseItemBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(
            snapshot: DocumentSnapshot,
            listener: onCourseSelectedListener?
        ) {
            val course = snapshot.toObject<Course>() ?: return
            binding.course = course

            binding.root.setOnClickListener{
                listener?.onCourseSelected(snapshot)
            }
        }
    }

}