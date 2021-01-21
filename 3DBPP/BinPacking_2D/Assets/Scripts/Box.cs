using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Box
{
    protected int length;
    protected int width;

    protected Transform prefab;
    protected Transform obj;

    public Box(int l, int w, GameObject _prefab)
    {
        length = l;
        width = w;

        prefab = _prefab.transform;
    }

    public int getLength() { return length; }
    public int getWidth() { return width; }

    protected void makeGameObject(Vector3 scale)
    {
        obj = MonoBehaviour.Instantiate(prefab, prefab.position, prefab.rotation);
        obj.transform.localScale = scale;

        obj.GetComponent<MeshRenderer>().material.color = getRandomColor();
    }

    public int getArea() { return length * width; }

    public Color getRandomColor()
    {
        Color color = new Color();

        color.r = Random.Range(0f, 1f);
        color.g = Random.Range(0f, 1f);
        color.b = Random.Range(0f, 1f);

        return color;
    }
}
