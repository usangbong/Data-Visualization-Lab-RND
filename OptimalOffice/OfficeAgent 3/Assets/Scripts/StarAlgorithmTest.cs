using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StarAlgorithmTest : MonoBehaviour
{
    const int UpRightToDownLeft = 1;
    const int UpLeftToDownRight = 2;
    const int DownRightToUpLeft = 3;
    const int DownLeftToUpRight = 4;

    public Transform Grid;
    private List<List<Transform>> cells;
    public Transform start, end;

    public float timeInterval;
    float time;

    private void Awake()
    {
        cells = new List<List<Transform>>();

        time = 0f;
    }

    void Start()
    {
        for(int i=0;i<Grid.childCount - 1;i++)
        {
            cells.Add(new List<Transform>());
            for(int j=0;j<Grid.GetChild(i).childCount;j++)
            {
                cells[i].Add(Grid.GetChild(i).GetChild(j));
                Grid.GetChild(i).GetChild(j).GetComponent<MeshRenderer>().material.color = Color.white;
            }
        }

        findPath(start, end);
    }

    private void Update()
    {
        
    }

    private float getHValue(Transform select)
    {
        float xInterval = Mathf.Abs(select.position.x - end.position.x);
        float yInterval = Mathf.Abs(select.position.y - end.position.y);

        return xInterval + yInterval;
    }

    private float getGValue(Transform select)
    {
        float xInterval = Mathf.Abs(select.position.x - start.position.x);
        float yInterval = Mathf.Abs(select.position.y - start.position.y);

        return xInterval + yInterval;
    }

    private List<Transform> findPath(Transform startNode, Transform endNode)
    {
        List<Transform> path = new List<Transform>();
        List<Transform> aroundNode;

        Transform currentNode = start;
        currentNode.GetComponent<MeshRenderer>().material.color = Color.black;

        path.Add(currentNode);

        bool obs = false;

        float x1 = startNode.position.x;
        float x2 = endNode.position.x;
        float z1 = startNode.position.z;
        float z2 = endNode.position.z;

        if (x1 > x2 && z1 > z2) //우상단 -> 좌하단
        {
            while (currentNode != endNode) 
            {
                aroundNode = getAroundNode(currentNode);
                currentNode = getNextTransform(aroundNode, UpRightToDownLeft, false);
                currentNode.GetComponent<MeshRenderer>().material.color = Color.black;
                path.Add(currentNode);


                /*if (isObstacle(currentNode))
                {
                    obs = true;
                    break;
                }*/
            }

            if (!obs)
            {
                Debug.Log(path.Count);
                return path;
            }

            path.Clear();
            currentNode = startNode;

            while (currentNode != endNode)
            {

            }
        }

        else if(x1 < x2 && z1 > z2) //좌상단 -> 우하단
        {

        }

        else if(x1 > x2 && z1 < z2) //우하단 -> 좌상단
        {

        }

        else if(x1 < x2 && z1 < z2) //좌하단 -> 우상단
        {

        }

        return path;
    }

    private List<Transform> getAroundNode(Transform currentNode)
    {
        List<Transform> aroundNode = new List<Transform>(); //up, down, left, right

        int x = findXindex(currentNode);
        int z = findZindex(currentNode);

        Transform up = currentNode.position.z + 1 > 0 ? null : cells[z - 1][x];
        Transform down = currentNode.position.z - 1 < -11 ? null : cells[z + 1][x];
        Transform left = currentNode.position.x - 1 < 0 ? null : cells[z][x - 1];
        Transform right = currentNode.position.x + 1 > 11 ? null : cells[z][x + 1];

        aroundNode.Add(up);
        aroundNode.Add(down);
        aroundNode.Add(left);
        aroundNode.Add(right);

        return aroundNode;
    }

    private int findXindex(Transform currentNode)
    {
        for(var i=0;i<cells.Count;i++)
        {
            for(var j=0;j<cells[i].Count;j++)
            {
                if (currentNode == cells[i][j]) return j;
            }
        }

        return -1;
    }

    private int findZindex(Transform currentNode)
    {
        for (var i = 0; i < cells.Count; i++)
        {
            for (var j = 0; j < cells[i].Count; j++)
            {
                if (currentNode == cells[i][j]) return i;
            }
        }

        return -1;
    }

    private Transform getNextTransform(List<Transform> aroundNode, int state, bool isObstacle)
    {
        List<Transform> sequenceNode = new List<Transform>();
        List<float> sequenceFvalue = new List<float>();

        Transform up = aroundNode[0];
        Transform down = aroundNode[1];
        Transform left = aroundNode[2];
        Transform right = aroundNode[3];

        float upFvalue = up == null ? Mathf.Infinity : getGValue(up) + getHValue(up);
        float downFvalue = down == null? Mathf.Infinity : getGValue(down) + getHValue(down);
        float leftFvalue = left == null? Mathf.Infinity : getGValue(left) + getHValue(left);
        float rightFvalue = right == null? Mathf.Infinity : getGValue(right) + getHValue(right);

        if(!isObstacle)
        {
            switch(state)
            {
                case UpRightToDownLeft:
                    sequenceNode.Add(left);
                    sequenceNode.Add(down);
                    sequenceNode.Add(right);
                    sequenceNode.Add(up);

                    sequenceFvalue.Add(leftFvalue);
                    sequenceFvalue.Add(downFvalue);
                    sequenceFvalue.Add(rightFvalue);
                    sequenceFvalue.Add(upFvalue);
                    break;
                case UpLeftToDownRight:
                    sequenceNode.Add(right);
                    sequenceNode.Add(down);
                    sequenceNode.Add(left);
                    sequenceNode.Add(up);

                    sequenceFvalue.Add(rightFvalue);
                    sequenceFvalue.Add(downFvalue);
                    sequenceFvalue.Add(leftFvalue);
                    sequenceFvalue.Add(upFvalue);
                    break;
                case DownRightToUpLeft:
                    sequenceNode.Add(left);
                    sequenceNode.Add(up);
                    sequenceNode.Add(right);
                    sequenceNode.Add(down);

                    sequenceFvalue.Add(leftFvalue);
                    sequenceFvalue.Add(upFvalue);
                    sequenceFvalue.Add(rightFvalue);
                    sequenceFvalue.Add(downFvalue);
                    break;
                case DownLeftToUpRight:
                    sequenceNode.Add(right);
                    sequenceNode.Add(up);
                    sequenceNode.Add(left);
                    sequenceNode.Add(down);

                    sequenceFvalue.Add(rightFvalue);
                    sequenceFvalue.Add(upFvalue);
                    sequenceFvalue.Add(leftFvalue);
                    sequenceFvalue.Add(downFvalue);
                    break;
                default:
                    break;
            }
        }

        else
        {
            switch(state)
            {
                case UpRightToDownLeft:
                    sequenceNode.Add(down);
                    sequenceNode.Add(left);
                    sequenceNode.Add(up);
                    sequenceNode.Add(right);

                    sequenceFvalue.Add(downFvalue);
                    sequenceFvalue.Add(leftFvalue);
                    sequenceFvalue.Add(upFvalue);
                    sequenceFvalue.Add(rightFvalue);
                    break;
                case UpLeftToDownRight:
                    sequenceNode.Add(down);
                    sequenceNode.Add(right);
                    sequenceNode.Add(up);
                    sequenceNode.Add(left);

                    sequenceFvalue.Add(downFvalue);
                    sequenceFvalue.Add(rightFvalue);
                    sequenceFvalue.Add(upFvalue);
                    sequenceFvalue.Add(leftFvalue);
                    break;
                case DownRightToUpLeft:
                    sequenceNode.Add(up);
                    sequenceNode.Add(left);
                    sequenceNode.Add(down);
                    sequenceNode.Add(right);

                    sequenceFvalue.Add(upFvalue);
                    sequenceFvalue.Add(leftFvalue);
                    sequenceFvalue.Add(downFvalue);
                    sequenceFvalue.Add(rightFvalue);
                    break;
                case DownLeftToUpRight:
                    sequenceNode.Add(up);
                    sequenceNode.Add(right);
                    sequenceNode.Add(down);
                    sequenceNode.Add(left);

                    sequenceFvalue.Add(upFvalue);
                    sequenceFvalue.Add(rightFvalue);
                    sequenceFvalue.Add(downFvalue);
                    sequenceFvalue.Add(leftFvalue);
                    break;
                default:
                    break;
            }
        }

        float minFvalue = 1000000;
        Transform minTransform = null;

        for (var i = 0; i < 4; i++)
        {
            if (sequenceFvalue[i] < minFvalue)
            {
                minFvalue = sequenceFvalue[i];
                minTransform = sequenceNode[i];
            }
        }

        return minTransform;
    }
    /*
    bool isEnd = false;

    private void Update()
    {
        time += Time.deltaTime;

        if(time > timeInterval)
        {
            isEnd = false;
        }

        if (isEnd) return;

        if(Input.GetKeyDown(KeyCode.Space))
        {
            isEnd = true;

            if (x1 > x2 && z1 > z2) //우상단 -> 좌하단
            {
                aroundNode = getAroundNode(currentNode);
                currentNode.GetComponent<MeshRenderer>().material.color = Color.white;
                currentNode = getNextTransform(aroundNode, UpRightToDownLeft, false);
                currentNode.GetComponent<MeshRenderer>().material.color = Color.black;
            }
        }
    }*/
}
