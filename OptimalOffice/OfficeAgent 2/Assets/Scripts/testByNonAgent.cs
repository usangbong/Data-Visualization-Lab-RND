using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.Reflection;

public class testByNonAgent : MonoBehaviour
{
    public List<GameObject> obj = new List<GameObject>();
    public OfficeArea area;

    void Start()
    {
        
    }

    void Update()
    {
        if(Input.GetKeyDown(KeyCode.Space))
        {
            var assembly = Assembly.GetAssembly(typeof(UnityEditor.Editor));
            var type = assembly.GetType("UnityEditor.LogEntries");
            var method = type.GetMethod("Clear");
            method.Invoke(new object(), null);

            area.CellReset();

            for (int i = 0; i < 4; i++)
            {
                makeDecision(obj[i]);
            }

            area.FindDuplicateCellAndDeductionToObject();
        }
    }

    void makeDecision(GameObject obj)
    {
        int action = Random.Range(0, 12);

        Cell cell = area.FindCellByIndex(action);
        cell.AddObject(obj);

        obj.transform.position = cell.getCenterPos();

        area.SearchOverTheCellObjectAndAddObjectToCell(cell, obj);
    }
}
