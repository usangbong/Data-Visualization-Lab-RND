using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MakeBackground : MonoBehaviour
{
    public GameObject String, ShadowPlane, BackGround, DownPlane;
    public GameObject Ikinema;
    public GameObject sp1, sp2, sp3, sp4, sp5;

    public bool firstPlaneSet, start, col;
    bool timeCor, timeCor2, BackgroundFin, timeBool2;
    bool timeBool, shadow, BackBool, RotateObj, IkinemaActive;
    public bool BackGroundFinish;

    public float time, time2;

    Vector3 rot;

    List<GameObject> stringList = new List<GameObject>();

    void Start()
    {
        for(int i=0;i<4;i++)
        {
            stringList.Add(Instantiate(String));
            stringList[i].SetActive(false);
        }
        start = col = BackgroundFin = BackGroundFinish = false;
        firstPlaneSet = timeCor = timeBool = shadow = false;
        BackBool = timeCor2 = RotateObj = false;
        time = time2 = 0;
        timeBool2 = IkinemaActive = false;

        rot = Vector3.up;
    }

    void Update()
    {
        if(start && !firstPlaneSet)
        {
            String.SetActive(false);
            for(int i=0;i<4;i++)
            {
                stringList[i].SetActive(true);
            }

            stringList[2].transform.localScale = new Vector3(0.1f, 0.1f, 1.1f);
            stringList[3].transform.localScale = new Vector3(0.1f, 0.1f, 1.1f);

            MoveObject(stringList[0], new Vector3(-0.07f, 0.006f, 1.146f));
            MoveObject(stringList[1], new Vector3(-0.067f, 1.906f, 1.146f));
            MoveObject(stringList[2], new Vector3(-1.48f, 1.056f, 1.146f));
            MoveObject(stringList[3], new Vector3(1.5f, 1.056f, 1.146f));

            RotateObject(stringList[0], new Vector3(0, 90f, 0));
            RotateObject(stringList[1], new Vector3(0, 90f, 0));
            RotateObject(stringList[2], new Vector3(90f, 90f, 0));
            RotateObject(stringList[3], new Vector3(90f, 90f, 0));

            if(stringList[0].transform.position == new Vector3(-0.07f, 0.006f, 1.146f) &&
                stringList[1].transform.position == new Vector3(-0.067f, 1.906f, 1.146f) &&
                stringList[2].transform.position == new Vector3(-1.48f, 1.056f, 1.146f) &&
                stringList[3].transform.position == new Vector3(1.5f, 1.056f, 1.146f))
            {
                firstPlaneSet = true;
            }
        }

        if(firstPlaneSet && !shadow && col)
        {
            for(int i=0;i<4;i++)
            {
                stringList[i].SetActive(false);
            }

            ShadowPlane.SetActive(true);

            if (!IkinemaActive)
            {
                Ikinema.SetActive(true);
            }

            SphereActive(false);

            if(!timeCor)
            {
                StartCoroutine(timeChecker());
                timeCor = true;
            }
        }

        if(shadow && !BackgroundFin)
        {
            ShadowPlane.SetActive(false);
            BackGround.SetActive(true);
            SphereActive(true);
            DownPlane.transform.SetParent(BackGround.transform);
            if(!BackBool)
            {
                StartCoroutine(MakeBack());
                StopCoroutine(timeChecker());
                BackBool = true;
            }
        }

        if(BackgroundFin && !RotateObj)
        {
            if(!timeCor2)
            {
                StartCoroutine(timeChecker2());
                timeCor2 = true;
            }
        }

        if(RotateObj && !BackGroundFinish)
        {
            BackGroundFinish = true;
        }
    }

    void MoveObject(GameObject obj, Vector3 toPos)
    {
        obj.transform.position = Vector3.MoveTowards(obj.transform.position,
            toPos, 1.0f * Time.deltaTime);
    }

    void RotateObject(GameObject obj, Vector3 toRot)
    {
        obj.transform.rotation = Quaternion.Slerp(obj.transform.rotation,
            Quaternion.Euler(toRot), 3.0f * Time.deltaTime);
    }

    void SphereActive(bool set)
    {
        sp1.SetActive(set);
        sp2.SetActive(set);
        sp3.SetActive(set);
        sp4.SetActive(set);
        sp5.SetActive(set);
    }

    IEnumerator timeChecker()
    {
        while(!timeBool)
        {
            time += 0.1f;

            if(time >= 45f)
            {
                Ikinema.SetActive(false);
                SphereActive(true);
                IkinemaActive = true;
            }

            if(time >= 90f)
            {
                shadow = true;
                timeBool = true;
            }

            yield return new WaitForSeconds(0.1f);
        }
    }

    IEnumerator timeChecker2()
    {
        while(!timeBool2)
        {
            time2 += 0.1f;

            if(time2>=5f)
            {
                timeBool2 = true;
                RotateObj = true;
            }

            yield return new WaitForSeconds(0.1f);
        }
    }

    IEnumerator MakeBack()
    {
        BackGround.transform.GetChild(1).gameObject.SetActive(true);
        yield return new WaitForSeconds(1.5f);
        BackGround.transform.GetChild(2).gameObject.SetActive(true);
        yield return new WaitForSeconds(1.5f);
        BackGround.transform.GetChild(3).gameObject.SetActive(true);
        yield return new WaitForSeconds(1.5f);
        BackGround.transform.GetChild(4).gameObject.SetActive(true);
        yield return new WaitForSeconds(1.5f);

        BackgroundFin = true;
    }
}
