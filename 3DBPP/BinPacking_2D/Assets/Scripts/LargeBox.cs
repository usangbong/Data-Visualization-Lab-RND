using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LargeBox : Box
{
    public List<MiddleBox> boxList;

    public LargeBox(int l, int w, GameObject prefab) : base(l, w, prefab)
    {
        boxList = new List<MiddleBox>();
    }

    public int getBoxCount()
    {
        return boxList.Count;
    }

    public void addBox(MiddleBox box)
    {
        boxList.Add(box);
    }

    public float getFillingRate()
    {
        float area = 0;
        for (int i = 0; i < boxList.Count; i++)
            area += boxList[i].getLength() * boxList[i].getWidth();

        return area / getArea();
    }

    public void Clear()
    {
        for (int i = 0; i < boxList.Count; i++)
            boxList[i].Clear();
        boxList.Clear();
    }

    public void MakeLargebox()
    {
        obj = MonoBehaviour.Instantiate(prefab);
        obj.transform.position = prefab.position;
    }
}
