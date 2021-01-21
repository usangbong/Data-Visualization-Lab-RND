using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MiddleBox : Box
{
    private Vector3 FLBPoint;

    public MiddleBox(int l, int w, GameObject prefab) : base(l, w, prefab)
    {
        Clear();
    }
    
    public Vector3 getFLBPoint() { return FLBPoint; }

    public void setFLBPoint(int x, int z)
    {
        FLBPoint.x = x;
        FLBPoint.y = 0;
        FLBPoint.z = z;
    }

    public void setObjectPoint(Vector3 pos) { FLBPoint = pos; }

    private Vector3 convertFLBToCenter()
    {
        Vector3 destPoint = Vector3.zero;

        destPoint.x = FLBPoint.x + (length / 2f);
        destPoint.y = FLBPoint.y;
        destPoint.z = FLBPoint.z + (width / 2f);

        return destPoint;
    }
    
    public void makeMiddleBoxObject()
    {
        makeGameObject(new Vector3(length, 0.05f, width));
        obj.transform.position = convertFLBToCenter();
    }

    public void Clear()
    {
        FLBPoint = Vector3.zero;

        if(obj != null) MonoBehaviour.Destroy(obj.gameObject);
    }
}
