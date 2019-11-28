using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEngine.SceneManagement;

public class MoveDotObject : MonoBehaviour
{
    public GameObject Blue, Yellow, Half, Ring;

    Heart heart;

    List<Vector3> BluePos = new List<Vector3>();
    List<Vector3> BlueRot = new List<Vector3>();
    List<Vector3> BlueScale = new List<Vector3>();

    List<Vector3> YellowPos = new List<Vector3>();
    List<Vector3> YellowRot = new List<Vector3>();
    List<Vector3> YellowScale = new List<Vector3>();

    List<Vector3> RingPos = new List<Vector3>();
    List<Vector3> RingRot = new List<Vector3>();
    List<Vector3> RingScale = new List<Vector3>();

    List<Vector3> HalfPos = new List<Vector3>();
    List<Vector3> HalfRot = new List<Vector3>();
    List<Vector3> HalfScale = new List<Vector3>();

    Vector3 pos, rot, scale;

    string BlueData, YellowData, HalfData, RingData;

    string[] splitDataToEnter;
    string[] splitDataToComma;

    public float speed;
    int cnt;
    bool isMove, isIn, isStart;

    char sp = '\n', sp2 = ',';

    void Start()
    {
        cnt = 0;
        isStart = isIn = isMove = false;
        speed = 1.0f;

        heart = GameObject.Find("HeartManager").GetComponent<Heart>();

        BlueData = LoadData("./Assets/Resources/Dot/blue.txt");
        YellowData = LoadData("./Assets/Resources/Dot/yellow.txt");
        HalfData = LoadData("./Assets/Resources/Dot/half.txt");
        RingData = LoadData("./Assets/Resources/Dot/ring.txt");

        BlueData = BlueData.Replace("(", "").Replace(")", "").Replace(" ", "");
        YellowData = YellowData.Replace("(", "").Replace(")", "").Replace(" ", "");
        HalfData = HalfData.Replace("(", "").Replace(")", "").Replace(" ", "");
        RingData = RingData.Replace("(", "").Replace(")", "").Replace(" ", "");

        splitDataToEnter = BlueData.Split(sp);
        for(int i=0;i<splitDataToEnter.Length -1; i++)
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

            BluePos.Add(pos);
            BlueRot.Add(rot);
            BlueScale.Add(scale);
        }

        splitDataToEnter = YellowData.Split(sp);
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

            YellowPos.Add(pos);
            YellowRot.Add(rot);
            YellowScale.Add(scale);
        }

        splitDataToEnter = RingData.Split(sp);
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

            RingPos.Add(pos);
            RingRot.Add(rot);
            RingScale.Add(scale);
        }

        splitDataToEnter = HalfData.Split(sp);
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

            HalfPos.Add(pos);
            HalfRot.Add(rot);
            HalfScale.Add(scale);
        }
    }

    
    void Update()
    {
        /*if(heart.isFinish)
        {
            if(!isStart)
            {
                isMove = isStart = true;
                StartCoroutine(MoveObject(Blue, BluePos, BlueRot, BlueScale, 0));
                StartCoroutine(MoveObject(Yellow, YellowPos, YellowRot, YellowScale, 0));
                StartCoroutine(MoveObject(Half, HalfPos, HalfRot, HalfScale, 0));
                StartCoroutine(MoveObject(Ring, RingPos, RingRot, RingScale, 0));
            }
        }*/
    }

    void SceneChange()
    {
        SceneManager.LoadScene("User Line Scene");
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
