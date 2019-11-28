using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class MovePlaneObject : MonoBehaviour
{
    public GameObject hide1, hide2, grid;

    PlaneObject plane;

    List<Vector3> hide1Pos = new List<Vector3>();
    List<Vector3> hide1Rot = new List<Vector3>();
    List<Vector3> hide1Scale = new List<Vector3>();

    List<Vector3> hide2Pos = new List<Vector3>();
    List<Vector3> hide2Rot = new List<Vector3>();
    List<Vector3> hide2Scale = new List<Vector3>();

    List<Vector3> gridPos = new List<Vector3>();
    List<Vector3> gridRot = new List<Vector3>();
    List<Vector3> gridScale = new List<Vector3>();

    Vector3 pos, rot, scale;

    string hide1Data, hide2Data, gridData;

    string[] splitDataToEnter;
    string[] splitDataToComma;

    public float speed;
    bool isMove, isIn, isStart;

    char sp = '\n', sp2 = ',';

    void Start()
    {
        isStart = isIn = isMove = false;
        speed = 1.0f;

        plane = GameObject.Find("GameObject").GetComponent<PlaneObject>();

        hide1Data = LoadData("./Assets/Resources/Plane/hide1.txt");
        hide2Data = LoadData("./Assets/Resources/Plane/hide2.txt");
        gridData = LoadData("./Assets/Resources/Plane/grid.txt");

        hide1Data = hide1Data.Replace("(", "").Replace(")", "").Replace(" ", "");
        hide2Data = hide2Data.Replace("(", "").Replace(")", "").Replace(" ", "");
        gridData = gridData.Replace("(", "").Replace(")", "").Replace(" ", "");

        splitDataToEnter = hide1Data.Split(sp);
        for (int i = 0; i < splitDataToEnter.Length - 1; i++)
        {
            splitDataToComma = splitDataToEnter[i].Split(sp2);

            pos = new Vector3(System.Convert.ToSingle(splitDataToComma[0]),
                System.Convert.ToSingle(splitDataToComma[1]),
                System.Convert.ToSingle(splitDataToComma[2]));

            rot = new Vector3(System.Convert.ToSingle(splitDataToComma[3]),
                System.Convert.ToSingle(splitDataToComma[4]),
                System.Convert.ToSingle(splitDataToComma[5]));

            scale = new Vector3(System.Convert.ToSingle(splitDataToComma[6]),
                System.Convert.ToSingle(splitDataToComma[7]),
                System.Convert.ToSingle(splitDataToComma[8]));

            hide1Pos.Add(pos);
            hide1Rot.Add(rot);
            hide1Scale.Add(scale);
        }

        splitDataToEnter = hide2Data.Split(sp);
        for (int i = 0; i < splitDataToEnter.Length - 1; i++)
        {
            splitDataToComma = splitDataToEnter[i].Split(sp2);

            pos = new Vector3(System.Convert.ToSingle(splitDataToComma[0]),
                System.Convert.ToSingle(splitDataToComma[1]),
                System.Convert.ToSingle(splitDataToComma[2]));

            rot = new Vector3(System.Convert.ToSingle(splitDataToComma[3]),
                System.Convert.ToSingle(splitDataToComma[4]),
                System.Convert.ToSingle(splitDataToComma[5]));

            scale = new Vector3(System.Convert.ToSingle(splitDataToComma[6]),
                System.Convert.ToSingle(splitDataToComma[7]),
                System.Convert.ToSingle(splitDataToComma[8]));

            hide2Pos.Add(pos);
            hide2Rot.Add(rot);
            hide2Scale.Add(scale);
        }

        splitDataToEnter = gridData.Split(sp);
        for (int i = 0; i < splitDataToEnter.Length - 1; i++)
        {
            splitDataToComma = splitDataToEnter[i].Split(sp2);

            pos = new Vector3(System.Convert.ToSingle(splitDataToComma[0]),
                System.Convert.ToSingle(splitDataToComma[1]),
                System.Convert.ToSingle(splitDataToComma[2]));

            rot = new Vector3(System.Convert.ToSingle(splitDataToComma[3]),
                System.Convert.ToSingle(splitDataToComma[4]),
                System.Convert.ToSingle(splitDataToComma[5]));

            scale = new Vector3(System.Convert.ToSingle(splitDataToComma[6]),
                System.Convert.ToSingle(splitDataToComma[7]),
                System.Convert.ToSingle(splitDataToComma[8]));

            gridPos.Add(pos);
            gridRot.Add(rot);
            gridScale.Add(scale);
        }
    }    

    void Update()
    {
        /*if(plane.fffff)
        {
            if(!isStart)
            {
                isMove = isStart = true;

                StartCoroutine(MoveObject(hide1, hide1Pos, hide1Rot, hide1Scale, 0));
                StartCoroutine(MoveObject(hide2, hide2Pos, hide2Rot, hide2Scale, 0));
                StartCoroutine(MoveObject(grid, gridPos, gridRot, gridScale, 0));
            }
        }*/
    }

    string LoadData(string path)
    {
        string data;

        FileStream f = new FileStream(path, FileMode.Open, FileAccess.Read);
        StreamReader reader = new StreamReader(f);
        data = reader.ReadToEnd();
        reader.Close();
        f.Close();

        return data;
    }

    IEnumerator MoveObject(GameObject obj, List<Vector3> pos, List<Vector3> rot, List<Vector3> scale, int num)
    {
        while (isMove)
        {
            if ((obj.transform.position.x == pos[pos.Count - 1].x &&
                obj.transform.position.y == pos[pos.Count - 1].y &&
                obj.transform.position.z == pos[pos.Count - 1].z) || num > pos.Count - 1)
            {
                //nothing
            }

            else
            {
                obj.transform.position = Vector3.MoveTowards(obj.transform.position, pos[num], speed * Time.deltaTime);
                obj.transform.rotation = Quaternion.Euler(rot[num].x, rot[num].y, rot[num].z);
                obj.transform.localScale = new Vector3(scale[num].x, scale[num].y, scale[num].x);
            }

            if (obj.transform.position.x == pos[num].x && obj.transform.position.y == pos[num].y &&
                obj.transform.position.z == pos[num].z)
            {
                num++;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }
}
