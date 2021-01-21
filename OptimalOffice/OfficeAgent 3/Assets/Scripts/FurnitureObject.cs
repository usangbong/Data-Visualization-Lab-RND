using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FurnitureObject : MonoBehaviour
{
    private List<Cell> markingCell;

    void Awake()
    {
        markingCell = new List<Cell>();
    }

    public List<Cell> getMarkingCell() { return markingCell; }

    public void clearMarkingCell() { markingCell.Clear(); }

    private void OnTriggerStay(Collider other)
    {
        if(other.tag == "cell")
            if(!markingCell.Contains(other.GetComponent<Cell>())) 
                markingCell.Add(other.GetComponent<Cell>());
    }
}
