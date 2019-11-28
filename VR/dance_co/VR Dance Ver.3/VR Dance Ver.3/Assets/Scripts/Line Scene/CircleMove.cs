using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CircleMove : MonoBehaviour
{
    public GameObject blueSphere, Wave, LL, SL;
    public GameObject waveIn1, waveIn2, waveIn3, waveIn4;
    
    public int cnt, colorNum, rotCnt, blueNum;
    public bool blueColliding, isMoveFinish, rotFinish;
    public bool isWaveMakeFinish, waveColorFinish, makeWaveFinish;
    public bool rot1, rot2, rot3, rot4, animFinish;

    int toNum, inToNum;

    PlayAnim anim;

    List<GameObject> waveInList = new List<GameObject>();

    void Start()
    {
        waveInList.Add(waveIn1);
        waveInList.Add(waveIn2);
        waveInList.Add(waveIn3);
        waveInList.Add(waveIn4);

        anim = GameObject.Find("WaveIn1").GetComponent<PlayAnim>();

        for(int i=0;i<4;i++)
        {
            for(int j=0;j<waveInList[i].transform.childCount;j++)
            {
                waveInList[i].transform.GetChild(j).gameObject.SetActive(false);
            }
        }

        toNum = inToNum = cnt = colorNum = rotCnt = blueNum = 0;
        blueColliding = isWaveMakeFinish = waveColorFinish = animFinish = false;
        rot1 = rot2 = rot3 = rot4 = rotFinish = makeWaveFinish = false;
        isMoveFinish = true;
    }

    void Update()
    {
        if (blueColliding && cnt < 4)
        {
            string path = "Path";
            path += (cnt + 1).ToString();
            itweenMove(path);
            blueColliding = false;
        }

        if (!isMoveFinish)
        {
            if (toNum >= 0 && toNum <= 11)
            {
                waveInList[cnt].transform.GetChild(toNum).gameObject.SetActive(true);
            }
        }

        if(cnt >= 4 && !isWaveMakeFinish)
        {
            blueSphere.SetActive(false);
            isWaveMakeFinish = true;
        }

        if(colorNum == 48)
        {
            waveColorFinish = true;
        }

        if(!rotFinish)
        {
            if(rot1)
            {
                waveIn1.transform.Rotate(Vector3.forward * 90f * Time.deltaTime);
            }

            if(rot2)
            {
                waveIn2.transform.Rotate(Vector3.forward * 90f * Time.deltaTime);
            }

            if(rot3)
            {
                waveIn3.transform.Rotate(Vector3.forward * 90f * Time.deltaTime);
            }

            if(rot4)
            {
                waveIn4.transform.Rotate(Vector3.forward * 90f * Time.deltaTime);
            }
        }

        if(rotCnt >= 4)
        {
            Invoke("RotFinish", 10.0f);
        }

        if(rotFinish && !makeWaveFinish)
        {
            Wave.transform.position = Vector3.MoveTowards(Wave.transform.position,
                new Vector3(0.155f, 1, 1), 2.0f * Time.deltaTime);
            Wave.transform.rotation = Quaternion.Slerp(Wave.transform.rotation,
                Quaternion.Euler(0, 0, 0), 3.0f * Time.deltaTime);
            waveIn1.transform.localRotation = Quaternion.Slerp(waveIn1.transform.localRotation,
                Quaternion.Euler(0, -90, 180), 1.0f * Time.deltaTime);
            waveIn2.transform.localRotation = Quaternion.Slerp(waveIn2.transform.localRotation,
                Quaternion.Euler(0, -90, 0), 1.0f * Time.deltaTime);
            waveIn3.transform.localRotation = Quaternion.Slerp(waveIn3.transform.localRotation,
                Quaternion.Euler(0, -90, 180), 1.0f * Time.deltaTime);
            waveIn4.transform.localRotation = Quaternion.Slerp(waveIn4.transform.localRotation,
                Quaternion.Euler(0, -90, 0), 1.0f * Time.deltaTime);

            Invoke("MakeFinish", 5.0f);
        }

        if(makeWaveFinish && !anim.animFinish)
        {
            waveIn1.transform.localRotation = Quaternion.Slerp(waveIn1.transform.localRotation,
                Quaternion.Euler(0, -90, 0), 5.0f * Time.deltaTime);
            waveIn3.transform.localRotation = Quaternion.Slerp(waveIn1.transform.localRotation,
                Quaternion.Euler(0, -90, 0), 5.0f * Time.deltaTime);
        }

        if(blueNum == 48 && !animFinish)
        {
            Invoke("AnimFin", 1.0f);
            Wave.SetActive(false);
            LL.SetActive(true);
            SL.SetActive(true);
        }
    }

    void itweenMove(string PathName)
    {
        iTween.MoveTo(blueSphere, iTween.Hash("path", iTweenPath.GetPath(PathName),
            "easeType", iTween.EaseType.linear, "time", 1.25f));
        iTween.ValueTo(gameObject, iTween.Hash("from", -3, "to", 12,
            "onupdate", "Counter", "time", 1.25f, "oncomplete", "CountFinish", "oncompletetarget", gameObject));
    }
    
    void Counter(int num)
    {
        toNum = num;
    }

    void CountFinish()
    {
        cnt++;
        isMoveFinish = true;
    }

    void RotFinish()
    {
        rotFinish = true;
    }

    void MakeFinish()
    {
        makeWaveFinish = true;
    }

    void AnimFin()
    {
        animFinish = true;
    }
}
