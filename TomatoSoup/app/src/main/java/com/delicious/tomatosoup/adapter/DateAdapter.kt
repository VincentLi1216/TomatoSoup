package com.delicious.tomatosoup.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.delicious.tomatosoup.databinding.DateItemBinding
import com.google.firebase.firestore.DocumentSnapshot
import com.google.firebase.firestore.Query

open class DateAdapter(query: Query, private val listener: onDateSelectedListener) :
    FirestoreAdapter<DateAdapter.DateViewHolder>(query) {

    interface onDateSelectedListener {
        fun onDateSelected(date: DocumentSnapshot)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): DateViewHolder {
        return DateViewHolder(DateItemBinding.inflate(
                LayoutInflater.from(parent.context), parent, false
            )
        )
    }

    override fun onBindViewHolder(holder: DateViewHolder, position: Int) {
        holder.bind(getSnapshot(position), listener)
    }

    class DateViewHolder(private val binding: DateItemBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(
            snapshot: DocumentSnapshot,
            listener: onDateSelectedListener?
        ) {
            binding.dateItemDate.text = snapshot.id

            binding.root.setOnClickListener{
                listener?.onDateSelected(snapshot)
            }
            binding.executePendingBindings()
        }
    }
}