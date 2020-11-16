using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Box : MonoBehaviour
{
    private int width;
    private int depth;
    private int height;
    private float weight;

    private Vector3 centerPoint;
    private Vector3 FLB;

    public Transform prefab;
    private Transform obj;

    public Box(int w, int d, int h, float g)
    {
        width = w;
        depth = d;
        height = h;
        weight = g;

        centerPoint = Vector3.zero;

        FLB.x = -width / 2f;
        FLB.y = -height / 2f;
        FLB.z = -depth / 2f;
    }

    public int getWidth() { return width; }
    public int getDepth() { return depth; }
    public int getHeight() { return height; }
    public float getWeight() { return weight; }
    public Vector3 getCenterPoint() { return centerPoint; }
    public Vector3 getFLB() { return FLB; }

    public int getVolume() { return width * depth * height; }
    
    //만들자 아래 두개 함수
    public void makeObject()
    {
        obj = Instantiate(prefab, prefab.position, prefab.rotation);
        obj.transform.localScale = new Vector3(width, height, depth);

        obj.transform.position = FLB;
    }

    private Vector3 convertFLBtoPoint()
    {
        Vector3 destPoint;

        return destPoint;
    }
}
