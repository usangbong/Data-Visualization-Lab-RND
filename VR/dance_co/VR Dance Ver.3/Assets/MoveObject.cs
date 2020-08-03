using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class MoveObject : MonoBehaviour
{
    public GameObject Cube, Sphere, Cylinder, Capsule, longCube;

    List<Vector3> CubePos = new List<Vector3>();
    List<Vector3> CubeRot = new List<Vector3>();
    List<Vector3> CubeScale = new List<Vector3>();

    List<Vector3> SpherePos = new List<Vector3>();
    List<Vector3> SphereRot = new List<Vector3>();
    List<Vector3> SphereScale = new List<Vector3>();

    List<Vector3> CylinderPos = new List<Vector3>();
    List<Vector3> CylinderRot = new List<Vector3>();
    List<Vector3> CylinderScale = new List<Vector3>();

    List<Vector3> CapsulePos = new List<Vector3>();
    List<Vector3> CapsuleRot = new List<Vector3>();
    List<Vector3> CapsuleScale = new List<Vector3>();

    List<Vector3> longCubePos = new List<Vector3>();
    List<Vector3> longCubeRot = new List<Vector3>();
    List<Vector3> longCubeScale = new List<Vector3>();

    Vector3 pos, rot, scale;

    string CubeData, SphereData, CylinderData, CapsuleData, longCubeData;

    string[] splitDataToEnter;
    string[] splitDataToComma;

    public float speed;
    public bool isMove;
    int cnt;
    bool isIn, isStart;

    char sp = '\n', sp2 = ',';

    private void Start()
    {
        cnt = 0;
        isStart = isIn = isMove = false;

        speed = 1.0f;

        CubeData = LoadData("./Assets/Resources/Cube.txt");
        SphereData = LoadData("./Assets/Resources/Sphere.txt");
        CylinderData = LoadData("./Assets/Resources/Cylinder.txt");
        CapsuleData = LoadData("./Assets/Resources/Capsule.txt");
        longCubeData = LoadData("./Assets/Resources/longCube.txt");

        CubeData = CubeData.Replace("(", "").Replace(")", "").Replace(" ", "");
        SphereData = SphereData.Replace("(", "").Replace(")", "").Replace(" ", "");
        CylinderData = CylinderData.Replace("(", "").Replace(")", "").Replace(" ", "");
        CapsuleData = CapsuleData.Replace("(", "").Replace(")", "").Replace(" ", "");
        longCubeData = longCubeData.Replace("(", "").Replace(")", "").Replace(" ", "");

        splitDataToEnter = CubeData.Split(sp);
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

            CubePos.Add(pos);
            CubeRot.Add(rot);
            CubeScale.Add(scale);
        }

        splitDataToEnter = SphereData.Split(sp);
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

            SpherePos.Add(pos);
            SphereRot.Add(rot);
            SphereScale.Add(scale);
        }

        splitDataToEnter = CylinderData.Split(sp);
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

            CylinderPos.Add(pos);
            CylinderRot.Add(rot);
            CylinderScale.Add(scale);
        }

        splitDataToEnter = CapsuleData.Split(sp);
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

            CapsulePos.Add(pos);
            CapsuleRot.Add(rot);
            CapsuleScale.Add(scale);
        }

        splitDataToEnter = longCubeData.Split(sp);
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

            longCubePos.Add(pos);
            longCubeRot.Add(rot);
            longCubeScale.Add(scale);
        }
    }

    private void Update()
    {
        if(!isStart && isMove)
        {
            isStart = true;
            StartCoroutine(MoveObjects(Cube, CubePos, CubeRot, CubeScale, 0));
            StartCoroutine(MoveObjects(Sphere, SpherePos, SphereRot, SphereScale, 0));
            StartCoroutine(MoveObjects(Cylinder, CylinderPos, CylinderRot, CylinderScale, 0));
            StartCoroutine(MoveObjects(Capsule, CapsulePos, CapsuleRot, CapsuleScale, 0));
            StartCoroutine(MoveObjects(longCube, longCubePos, longCubeRot, longCubeScale, 0));
        }
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

    IEnumerator MoveObjects(GameObject obj, List<Vector3> pos, List<Vector3> rot, List<Vector3> scale, int num)
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
                    iss = true;
                    cnt++;
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