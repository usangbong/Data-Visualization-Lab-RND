using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMove_one : MonoBehaviour
{
    public Transform glassTable;
    public Transform Sofa;
    public Transform Bed;
    public Transform Table;
    public Transform Closet;
    public Transform BedCabinet;
    public Transform SofaCabinet;

    Transform collidingObject;

    List<Transform> moveList = new List<Transform>();

    [HideInInspector]
    public bool isMoveFinish = false;
    [HideInInspector]
    public int finIdx = 0;
    int idx = 0;

    int collidingCount = 0;

    private void Awake()
    {
        moveList.Add(Sofa);
        moveList.Add(Table);
        moveList.Add(Sofa);
        moveList.Add(Bed);
        moveList.Add(Closet);
        moveList.Add(Table);
        moveList.Add(SofaCabinet);
        moveList.Add(Sofa);

        resetPos();
    }

    private void Update()
    {
        moveToObject();
    }

    void moveToObject()
    {
        transform.position = Vector3.MoveTowards(transform.position, moveList[idx].position, 10.0f * Time.deltaTime);

        if (transform.position == moveList[idx].position)
        {
            idx++;
        }

        if (idx > moveList.Count - 1)
        {
            idx = 0;
            isMoveFinish = true;
            resetPos();
        }
    }

    public void resetPos()
    {
        transform.position = new Vector3(9.3f, 1.6f, -7.2f);
        collidingCount = 0;
    }

    public string collidingName()
    {
        if (collidingObject == null) return "None";

        if (collidingObject.name == moveList[idx].name) return "None";
        else return collidingObject.name;
    }

    public void addCount()
    {
        collidingCount = collidingCount + 1;
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "moveObject")
        {
            collidingObject = other.gameObject.transform;
        }
    }
}
