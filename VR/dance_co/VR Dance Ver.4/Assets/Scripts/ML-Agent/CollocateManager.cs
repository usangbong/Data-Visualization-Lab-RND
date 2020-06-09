using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CollocateManager : MonoBehaviour
{
    public Transform pivot, target;
    public GameObject parent;

    List<Vector3> originPos = new List<Vector3>(), originRot = new List<Vector3>();
    List<GameObject> objList = new List<GameObject>();
    List<bool> objMoveList = new List<bool>();

    Vector2 tallX, tallY, tallZ;
    Vector2 shortX, shortY, shortZ;

    float xPos, yPos, zPos, speed;

    bool isTall = false, isFast = false, isWide = false;

    void Start()
    {
        for(var i=0;i<parent.transform.childCount;i++)
        {
            objList.Add(parent.transform.GetChild(i).gameObject);
            originPos.Add(parent.transform.GetChild(i).transform.position);
            originRot.Add(parent.transform.GetChild(i).transform.rotation.eulerAngles);
            objMoveList.Add(false);
        }

        tallX = new Vector2(-2f, 2f);
        tallY = new Vector2(1f, 2f);
        tallZ = new Vector2(-1.5f, 1.5f);

        shortX = new Vector2(-0.5f, 0.5f);
        shortY = new Vector2(0f, 1f);
        shortZ = new Vector2(-0.35f, 0.35f);
    }

    void Update()
    {
        for(var i=0;i<objList.Count;i++)
        {
            if(isOverPos(objList[i], 'x')) targetReset(objList[i], i);
            if(isOverPos(objList[i], 'y')) targetReset(objList[i], i);
            if(isOverPos(objList[i], 'z')) targetReset(objList[i], i);
        }

        for (var i = 0; i < objList.Count; i++)
        {
            if (!objMoveList[i])
            {
                Vector3 targetPos, startTan, endTan;
                if (isTall)
                {
                    targetPos = getRandomPos(tallX, tallY, tallZ);
                    startTan = getRandomPos(tallX, tallY, tallZ);
                    endTan = getRandomPos(tallX, tallY, tallZ);

                    speed = Random.Range(0.001f, 0.02f);
                }

                else
                {
                    targetPos = getRandomPos(shortX, shortY, shortZ);
                    startTan = getRandomPos(shortX, shortY, shortZ);
                    endTan = getRandomPos(shortX, shortY, shortZ);

                    speed = Random.Range(0.02f, 0.1f);
                }

                objMoveList[i] = true;

                StartCoroutine(moveObject(objList[i], originPos[i], startTan, endTan, targetPos, speed, i));
            }
        }
    }

    Vector3 getRandomPos(Vector2 xPos, Vector2 yPos, Vector2 zPos)
    {
        float x = Random.Range(xPos.x, xPos.y);
        float y = Random.Range(yPos.x, yPos.y);
        float z = Random.Range(zPos.x, zPos.y);

        x = Mathf.Round(x * 100) * 0.01f;
        y = Mathf.Round(y * 100) * 0.01f;
        z = Mathf.Round(z * 100) * 0.01f;

        return new Vector3(x, y, z);
    }

    void targetReset(GameObject obj, int idx)
    {
        obj.transform.position = originPos[idx];
        obj.transform.rotation = Quaternion.Euler(originRot[idx]);
        objMoveList[idx] = false;
    }

    bool isOverPos(GameObject obj, char posIdx)
    {
        if (posIdx == 'x')
        {
            if (obj.transform.position.x >= pivot.position.x + 2f || obj.transform.position.x <= pivot.position.x - 2f) return true;
            else return false;
        }

        else if (posIdx == 'y')
        {
            if (obj.transform.position.y >= 2.2f || obj.transform.position.y <= -0.5f) return true;
            else return false;
        }

        else if (posIdx == 'z')
        {
            if (obj.transform.position.z >= pivot.position.z + 1.5f || obj.transform.position.z <= pivot.position.z - 1.5f) return true;
            else return false;
        }

        else return true;
    }

    Vector3 getBezierCurve(Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3, float t)
    {
        float u = 1f - t;
        float t2 = t * t;
        float u2 = u * u;
        float u3 = u2 * u;
        float t3 = t2 * t;

        Vector3 result = u3 * p0 + 3f * u2 * t * p1 + 3f * u * t2 * p2 + t3 * p3;

        return result;
    }

    public void setTall(bool tall)
    {
        isTall = tall;
    }

    public void setFast(bool fast)
    {
        isFast = fast;
    }

    public void setWide(bool wide)
    {
        isWide = wide;
    }

    IEnumerator moveObject(GameObject obj, Vector3 originPos, Vector3 startTan, Vector3 endTan, Vector3 targetPos, float speed, int idx)
    {
        speed = Mathf.Round(speed * 1000) * 0.001f;

        for(var t=0f;t<=1f;t+=0.01f)
        {
            obj.transform.position = getBezierCurve(originPos, startTan, endTan, targetPos, t);
            yield return new WaitForSeconds(speed);
        }

        objMoveList[idx] = false;
    }
}
