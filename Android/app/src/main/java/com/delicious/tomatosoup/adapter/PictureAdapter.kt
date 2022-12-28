package com.delicious.tomatosoup.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.ImageView
import androidx.core.net.toUri
import androidx.databinding.BindingAdapter
import androidx.recyclerview.widget.RecyclerView
import coil.load
import com.delicious.tomatosoup.R
import com.delicious.tomatosoup.databinding.PictureItemBinding
import com.delicious.tomatosoup.model.Picture
import com.google.firebase.firestore.DocumentSnapshot
import com.google.firebase.firestore.Query
import com.google.firebase.firestore.ktx.toObject

open class PictureAdapter(query: Query, private val listener: onPictureSelectedListener) :
    FirestoreAdapter<PictureAdapter.PictureViewHolder>(query) {

    interface onPictureSelectedListener {
        fun onPictureSelected(date: DocumentSnapshot)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PictureAdapter.PictureViewHolder {
        return PictureAdapter.PictureViewHolder(
            PictureItemBinding.inflate(
                LayoutInflater.from(parent.context), parent, false
            )
        )
    }

    override fun onBindViewHolder(holder: PictureViewHolder, position: Int) {
        holder.bind(getSnapshot(position), listener)
    }

    class PictureViewHolder(private val binding: PictureItemBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(
            snapshot: DocumentSnapshot,
            listener: PictureAdapter.onPictureSelectedListener?
        ) {
            val picture = snapshot.toObject<Picture>() ?: return
//            binding.picture = picture
            binding.picture = Picture("https://images.unsplash.com/photo-1665659145984-2d474f053e2d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1287&q=80")
            binding.root.setOnClickListener{
                listener?.onPictureSelected(snapshot)
            }
            binding.executePendingBindings()
        }
    }
}

@BindingAdapter("imageUrl")
fun bindImage(imgView: ImageView, imgUrl: String?) {
    imgUrl?.let {
        val imgUri = imgUrl.toUri().buildUpon().scheme("https").build()
        imgView.load(imgUri) {
            error(R.drawable.ic_baseline_broken_image_24)
        }
    }
}