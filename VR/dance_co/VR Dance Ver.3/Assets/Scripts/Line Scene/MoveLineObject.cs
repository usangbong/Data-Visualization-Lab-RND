using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Valve.VR;
using System.IO;
using UnityEngine.SceneManagement;

public class MoveLineObject : MonoBehaviour
{
    public GameObject Line, Arrows, Cube1, Cube2;

    int cnt;
    public bool isFin;

    List<Vector3> LinePos = new List<Vector3>();
    List<Vector3> LineRot = new List<Vector3>();
    List<Vector3> LineScale = new List<Vector3>();

    List<Vector3> ArrowPos = new List<Vector3>();
    List<Vector3> ArrowRot = new List<Vector3>();
    List<Vector3> ArrowScale = new List<Vector3>();

    List<Vector3> Cube1Pos = new List<Vector3>();
    List<Vector3> Cube1Rot = new List<Vector3>();
    List<Vector3> Cube1Scale = new List<Vector3>();

    List<Vector3> Cube2Pos = new List<Vector3>();
    List<Vector3> Cube2Rot = new List<Vector3>();
    List<Vector3> Cube2Scale = new List<Vector3>();

    Vector3 pos, rot, scale;

    string LineData, ArrowData, Cube1Data, Cube2Data;

    string[] splitDataToEnter;
    string[] splitDataToComma;

    public float speed;
    bool isMove, isIn, isStart;

    char sp = '\n', sp2 = ',';

    void Start()
    {
        isStart = isIn = isMove = false;
        speed = 1.0f;

        cnt = 0;
        isFin = false;

        LineData = LoadData("./Assets/Resources/Dot/blue.txt");
        ArrowData = LoadData("./Assets/Resources/Dot/yellow.txt");
        Cube1Data = LoadData("./Assets/Resources/Dot/half.txt");
        Cube2Data = LoadData("./Assets/Resources/Dot/ring.txt");

        LineData = LineData.Replace("(", "").Replace(")", "").Replace(" ", "");
        ArrowData = ArrowData.Replace("(", "").Replace(")", "").Replace(" ", "");
        Cube1Data = Cube1Data.Replace("(", "").Replace(")", "").Replace(" ", "");
        Cube2Data = Cube2Data.Replace("(", "").Replace(")", "").Replace(" ", "");

        splitDataToEnter = LineData.Split(sp);
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

            LinePos.Add(pos);
            LineRot.Add(rot);
            LineScale.Add(scale);
        }

        splitDataToEnter = ArrowData.Split(sp);
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

            ArrowPos.Add(pos);
            ArrowRot.Add(rot);
            ArrowScale.Add(scale);
        }

        splitDataToEnter = Cube1Data.Split(sp);
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

            Cube1Pos.Add(pos);
            Cube1Rot.Add(rot);
            Cube1Scale.Add(scale);
        }

        splitDataToEnter = Cube2Data.Split(sp);
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

            Cube2Pos.Add(pos);
            Cube2Rot.Add(rot);
            Cube2Scale.Add(scale);
        }
    }


    void Update()
    {
        if(cnt >= 4)
        {
            isFin = true;
            //Invoke("SceneChange", 10.0f);
        }

        /*if (ar.isFin)
        {
            if (!isStart)
            {
                isMove = isStart = true;
                StartCoroutine(MoveObject(Line, LinePos, LineRot, LineScale, 0));
                StartCoroutine(MoveObject(Arrows, ArrowPos, ArrowRot, ArrowScale, 0));
                StartCoroutine(MoveObject(Cube1, Cube1Pos, Cube1Rot, Cube1Scale, 0));
                StartCoroutine(MoveObject(Cube2, Cube2Pos, Cube2Rot, Cube2Scale, 0));
            }
        }*/
    }

    void SceneChange()
    {
        SceneManager.LoadScene("User Plane Scene");
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
        bool iss = false;
        while (isMove)
        {
            if ((obj.transform.position.x == pos[pos.Count - 1].x &&
                obj.transform.position.y == pos[pos.Count - 1].y &&
                obj.transform.position.z == pos[pos.Count - 1].z) || num > pos.Count - 1)
            {
                if (!iss)
                {
                    cnt++;
                    iss = true;
                }
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
