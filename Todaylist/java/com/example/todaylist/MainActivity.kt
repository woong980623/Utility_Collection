package com.example.todaylist

import android.os.Bundle
import android.text.InputType
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.ImageButton
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.floatingactionbutton.FloatingActionButton

class MainActivity : AppCompatActivity() {

    private lateinit var tdlList: MutableList<String>
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: TdlAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tdlList = mutableListOf()

        recyclerView = findViewById(R.id.recyclerView)
        recyclerView.layoutManager = LinearLayoutManager(this)

        adapter = TdlAdapter(tdlList)
        recyclerView.adapter = adapter

        val fab: FloatingActionButton = findViewById(R.id.fab)
        fab.setOnClickListener { showAddTaskDialog() }
    }

    private fun showAddTaskDialog() {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Add New Task")

        val input = EditText(this)
        input.inputType = InputType.TYPE_CLASS_TEXT
        builder.setView(input)

        builder.setPositiveButton("Add") { dialog, _ ->
            val task = input.text.toString()
            if (task.isNotEmpty()) {
                tdlList.add(task)
                adapter.notifyItemInserted(tdlList.size - 1)
            }
            dialog.dismiss()
        }

        builder.setNegativeButton("Cancel") { dialog, _ -> dialog.cancel() }

        builder.show()
    }
}

class TdlAdapter(private val tdlList: MutableList<String>) :
    RecyclerView.Adapter<TdlAdapter.TdlViewHolder>() {

    inner class TdlViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val taskTextView: TextView = itemView.findViewById(R.id.taskTextView)
        val deleteButton: ImageButton = itemView.findViewById(R.id.deleteButton)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): TdlViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_tdl, parent, false)
        return TdlViewHolder(view)
    }

    override fun onBindViewHolder(holder: TdlViewHolder, position: Int) {
        val task = tdlList[position]
        holder.taskTextView.text = task

        holder.deleteButton.setOnClickListener {
            tdlList.removeAt(position)
            notifyItemRemoved(position)
            notifyItemRangeChanged(position, tdlList.size)
        }
    }

    override fun getItemCount(): Int {
        return tdlList.size
    }
}
