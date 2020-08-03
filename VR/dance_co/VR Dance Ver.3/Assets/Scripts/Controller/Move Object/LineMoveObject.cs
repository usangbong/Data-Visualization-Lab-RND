using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Valve.VR;
using System.IO;
using UnityEngine.SceneManagement;

public class LineMoveObject : MonoBehaviour
{
    public SteamVR_Input_Sources handType;
    public SteamVR_Behaviour_Pose controllerPose;
    public SteamVR_Action_Boolean teleportAction;
    public SteamVR_Action_Boolean grabGripAction;
    public SteamVR_Action_Boolean menuAction;
    public SteamVR_Action_Vector2 teleportPos;

    public GameObject MenuObject, laserPrefab;
    public GameObject Line, Arrows, Cube1, Cube2;

    GameObject pre_L, pre_A, pre_C1, pre_C2;

    GameObject laser, SelectObject, SelectPrefab;
    Transform laserTransform, lastTransform;
    Vector3 hitPoint;
    Vector2 touchValue;

    string Paths;

    Grab grab;

    List<Vector3> posList = new List<Vector3>();
    List<Vector3> rotList = new List<Vector3>();
    List<Vector3> scaleList = new List<Vector3>();
    List<string> moveDataList = new List<string>();

    FileStream file;
    StreamWriter writer;

    float start, end, diff, speed, size;
    int num;
    string names;
    bool isMoveStart, isPlay, isSpeed, isPre, aa, isSize, isPrefab, isThick;

    void Start()
    {
        laser = Instantiate(laserPrefab);
        laserTransform = laser.transform;
        MenuObject.SetActive(false);

        isMoveStart = isPlay = isSpeed = isPre = aa = isSize = isPrefab = isThick = false;

        if (handType == SteamVR_Input_Sources.LeftHand)
        {
            grab = GameObject.Find("Controller (left)").GetComponent<Grab>();
        }

        else if (handType == SteamVR_Input_Sources.RightHand)
        {
            grab = GameObject.Find("Controller (right)").GetComponent<Grab>();
        }

        num = 0;
        speed = 1.0f;
        size = 0.0f;
        SelectObject = null;

        Paths = "";
    }

    void Update()
    {
        if (!isPre)
        {
            pre_L = Instantiate(Line);
            pre_A = Instantiate(Arrows);
            pre_C1 = Instantiate(Cube1);
            pre_C2 = Instantiate(Cube2);

            ColorToBlue(pre_L);
            ColorToBlue(pre_A);
            ColorToBlue(pre_C1);
            ColorToBlue(pre_C2);

            pre_L.SetActive(false);
            pre_A.SetActive(false);
            pre_C1.SetActive(false);
            pre_C2.SetActive(false);

            isPre = true;
        }

        if (SelectObject != null)
        {
            names = "SelectObject : ";
            names += SelectObject.name;
            MenuObject.transform.GetChild(6).GetComponent<TextMesh>().text = names;
        }

        RaycastHit hit;

        if (Physics.Raycast(controllerPose.transform.position, transform.forward, out hit, 100))
        {
            hitPoint = hit.point;
            if (hit.transform.tag == "Controller")
            {
                laser.SetActive(false);
            }

            else ShowLaser(hit);

            if (hit.transform.tag == "Line")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    Line.GetComponent<CapsuleCollider>().isTrigger = false;
                    Line.GetComponent<Rigidbody>().isKinematic = false;
                    Arrows.GetComponent<BoxCollider>().isTrigger = true;
                    Arrows.GetComponent<Rigidbody>().isKinematic = true;
                    Cube1.GetComponent<BoxCollider>().isTrigger = true;
                    Cube1.GetComponent<Rigidbody>().isKinematic = true;
                    Cube2.GetComponent<BoxCollider>().isTrigger = true;
                    Cube2.GetComponent<Rigidbody>().isKinematic = true;
                    SelectObject = Line;
                    SelectPrefab = pre_L;
                    posList.Clear();
                    rotList.Clear();
                    scaleList.Clear();
                    moveDataList.Clear();
                    MenuObject.SetActive(true);
                    lastTransform = null;
                    speed = 1.0f;
                    size = 0.0f;
                    isMoveStart = isPlay = isSpeed = isSize = isPrefab = isThick = aa = false;
                }
            }

            if (hit.transform.tag == "Arrow")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    Line.GetComponent<CapsuleCollider>().isTrigger = true;
                    Line.GetComponent<Rigidbody>().isKinematic = true;
                    Arrows.GetComponent<BoxCollider>().isTrigger = false;
                    Arrows.GetComponent<Rigidbody>().isKinematic = false;
                    Cube1.GetComponent<BoxCollider>().isTrigger = true;
                    Cube1.GetComponent<Rigidbody>().isKinematic = true;
                    Cube2.GetComponent<BoxCollider>().isTrigger = true;
                    Cube2.GetComponent<Rigidbody>().isKinematic = true;
                    SelectObject = Arrows;
                    SelectPrefab = pre_A;
                    posList.Clear();
                    rotList.Clear();
                    scaleList.Clear();
                    moveDataList.Clear();
                    MenuObject.SetActive(true);
                    lastTransform = null;
                    speed = 1.0f;
                    size = 0.0f;
                    isMoveStart = isPlay = isSpeed = isSize = isPrefab = isThick = aa = false;
                }
            }

            if (hit.transform.tag == "Cube1")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    Line.GetComponent<CapsuleCollider>().isTrigger = true;
                    Line.GetComponent<Rigidbody>().isKinematic = true;
                    Arrows.GetComponent<BoxCollider>().isTrigger = true;
                    Arrows.GetComponent<Rigidbody>().isKinematic = true;
                    Cube1.GetComponent<BoxCollider>().isTrigger = false;
                    Cube1.GetComponent<Rigidbody>().isKinematic = false;
                    Cube2.GetComponent<BoxCollider>().isTrigger = true;
                    Cube2.GetComponent<Rigidbody>().isKinematic = true;
                    SelectObject = Cube1;
                    SelectPrefab = pre_C1;
                    posList.Clear();
                    rotList.Clear();
                    scaleList.Clear();
                    moveDataList.Clear();
                    MenuObject.SetActive(true);
                    lastTransform = null;
                    speed = 1.0f;
                    size = 0.0f;
                    isMoveStart = isPlay = isSpeed = isSize = isPrefab = isThick = aa = false;
                }
            }

            if (hit.transform.tag == "Cube2")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    Line.GetComponent<CapsuleCollider>().isTrigger = true;
                    Line.GetComponent<Rigidbody>().isKinematic = true;
                    Arrows.GetComponent<BoxCollider>().isTrigger = true;
                    Arrows.GetComponent<Rigidbody>().isKinematic = true;
                    Cube1.GetComponent<BoxCollider>().isTrigger = true;
                    Cube1.GetComponent<Rigidbody>().isKinematic = true;
                    Cube2.GetComponent<BoxCollider>().isTrigger = false;
                    Cube2.GetComponent<Rigidbody>().isKinematic = false;
                    SelectObject = Cube2;
                    SelectPrefab = pre_C2;
                    posList.Clear();
                    rotList.Clear();
                    scaleList.Clear();
                    moveDataList.Clear();
                    MenuObject.SetActive(true);
                    lastTransform = null;
                    speed = 1.0f;
                    size = 0.0f;
                    isMoveStart = isPlay = isSpeed = isSize = isPrefab = isThick = aa = false;
                }
            }

            if (hit.transform.tag == "Size")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    if (!isSize)
                    {
                        isSize = true;
                        MenuObject.transform.GetChild(2).GetComponent<MeshRenderer>().material.color = Color.yellow;
                    }

                    else
                    {
                        isSize = false;
                        MenuObject.transform.GetChild(2).GetComponent<MeshRenderer>().material.color = Color.black;
                    }
                }
            }

            if (hit.transform.tag == "Save")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    Paths = "./Assets/Data/Line/";
                    MenuObject.transform.GetChild(3).GetComponent<MeshRenderer>().material.color = Color.yellow;
                    Invoke("saveBlack", 0.5f);

                    if (SelectObject.transform.name == "ArrowParent")
                    {
                        SaveData("./Assets/Resources/Line/arrow.txt");
                        Paths += "arrow";
                        Paths += System.DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss");
                        Paths += ".txt";
                        SaveData(Paths);
                    }
                    
                    else if (SelectObject.transform.name == "upColor1")
                    {
                        SaveData("./Assets/Resources/Line/line.txt");
                        Paths += "line";
                        Paths += System.DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss");
                        Paths += ".txt";
                        SaveData(Paths);
                    }

                    else if (SelectObject.transform.name == "CubeLine1")
                    {
                        SaveData("./Assets/Resources/Line/cube1.txt");
                        Paths += "cube1";
                        Paths += System.DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss");
                        Paths += ".txt";
                        SaveData(Paths);
                    }

                    else if (SelectObject.transform.name == "CubeLine2")
                    {
                        SaveData("./Assets/Resources/Line/cube2.txt");
                        Paths += "cube2";
                        Paths += System.DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss");
                        Paths += ".txt";
                        SaveData(Paths);
                    }
                }
            }


            if (hit.transform.tag == "Thick")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    if (!isThick)
                    {
                        MenuObject.transform.GetChild(7).GetComponent<MeshRenderer>().material.color = Color.yellow;
                        isThick = true;
                    }

                    else
                    {
                        MenuObject.transform.GetChild(7).GetComponent<MeshRenderer>().material.color = Color.black;
                        isThick = false;
                    }
                }
            }

            if (hit.transform.tag == "Reset")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    MenuObject.transform.GetChild(4).GetComponent<MeshRenderer>().material.color = Color.yellow;
                    posList.Clear();
                    rotList.Clear();
                    scaleList.Clear();
                    moveDataList.Clear();
                    num = 0;

                    SelectObject.transform.position = lastTransform.position;
                    SelectObject.transform.rotation = lastTransform.rotation;
                    SelectObject.transform.localScale = lastTransform.localScale;

                    SelectObject.SetActive(true);
                    SelectPrefab.SetActive(false);

                    if(SelectObject.name == "upColor1")
                    {
                        SelectObject.GetComponent<CapsuleCollider>().isTrigger = false;
                        SelectObject.GetComponent<Rigidbody>().isKinematic = false;
                        SelectPrefab.GetComponent<CapsuleCollider>().isTrigger = true;
                        SelectPrefab.GetComponent<Rigidbody>().isKinematic = true;
                    }

                    else
                    {
                        SelectObject.GetComponent<BoxCollider>().isTrigger = false;
                        SelectObject.GetComponent<Rigidbody>().isKinematic = false;
                        SelectPrefab.GetComponent<BoxCollider>().isTrigger = true;
                        SelectPrefab.GetComponent<Rigidbody>().isKinematic = true;
                    }

                    Invoke("resetBlack", 0.5f);

                    speed = 1.0f;
                    size = 0.0f;
                    isMoveStart = isPlay = isSpeed = isSize = isPrefab = isThick = aa = false;
                }
            }

            if (hit.transform.tag == "Play")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    Line.GetComponent<CapsuleCollider>().isTrigger = true;
                    Line.GetComponent<Rigidbody>().isKinematic = true;
                    Arrows.GetComponent<BoxCollider>().isTrigger = true;
                    Arrows.GetComponent<Rigidbody>().isKinematic = true;
                    Cube1.GetComponent<BoxCollider>().isTrigger = true;
                    Cube1.GetComponent<Rigidbody>().isKinematic = true;
                    Cube2.GetComponent<BoxCollider>().isTrigger = true;
                    Cube2.GetComponent<Rigidbody>().isKinematic = true;

                    if (SelectObject.name == "upColor1")
                    {
                        SelectPrefab.GetComponent<CapsuleCollider>().isTrigger = true;
                        SelectPrefab.GetComponent<Rigidbody>().isKinematic = true;
                    }

                    else
                    {
                        SelectPrefab.GetComponent<BoxCollider>().isTrigger = true;
                        SelectPrefab.GetComponent<Rigidbody>().isKinematic = true;
                    }

                    MenuObject.transform.GetChild(1).GetComponent<MeshRenderer>().material.color = Color.yellow;
                    DecodeTransformData();
                    SelectPrefab.SetActive(false);

                    SelectObject.transform.position = lastTransform.position;
                    SelectObject.transform.rotation = lastTransform.rotation;
                    SelectObject.transform.localScale = lastTransform.localScale;
                    isPlay = true;
                    isPrefab = false;
                    num = 0;

                    SelectObject.SetActive(true);
                }
            }

            if (hit.transform.tag == "User")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    SceneManager.LoadScene("User Line Scene");
                }
            }

            if (hit.transform.tag == "Esc")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    if(SelectObject.name == "upColor1")
                    {
                        SelectObject.GetComponent<CapsuleCollider>().isTrigger = true;
                        SelectObject.GetComponent<Rigidbody>().isKinematic = true;
                        SelectPrefab.GetComponent<CapsuleCollider>().isTrigger = true;
                        SelectPrefab.GetComponent<Rigidbody>().isKinematic = true;
                    }

                    else
                    {
                        SelectObject.GetComponent<BoxCollider>().isTrigger = true;
                        SelectObject.GetComponent<Rigidbody>().isKinematic = true;
                        SelectPrefab.GetComponent<BoxCollider>().isTrigger = true;
                        SelectPrefab.GetComponent<Rigidbody>().isKinematic = true;
                    }

                    SelectPrefab.SetActive(false);
                    SelectObject.SetActive(true);

                    SelectPrefab = null;
                    SelectObject = null;

                    posList.Clear();
                    rotList.Clear();

                    scaleList.Clear();

                    isSize = false;

                    MenuObject.SetActive(false);
                    lastTransform = null;
                    moveDataList.Clear();

                    speed = 1.0f;
                    size = 0.0f;
                    isMoveStart = isPlay = isSpeed = isSize = isPrefab = isThick = aa = false;
                }
            }
        }

        else
        {
            laser.SetActive(false);
        }

        if (isPlay && posList.Count > 0)
        {
            SelectObject.transform.position = Vector3.MoveTowards(SelectObject.transform.position,
                posList[num], speed * Time.deltaTime);
            SelectObject.transform.rotation = Quaternion.Euler(rotList[num]);
            SelectObject.transform.localScale = new Vector3(scaleList[num].x, scaleList[num].y, scaleList[num].z);

            if (SelectObject.transform.position.x == posList[num].x &&
                SelectObject.transform.position.y == posList[num].y &&
                SelectObject.transform.position.z == posList[num].z)
            {
                num++;
            }

            if (SelectObject.transform.position == posList[posList.Count - 1])
            {
                MenuObject.transform.GetChild(1).GetComponent<MeshRenderer>().material.color = Color.black;
                isPlay = false;

                if(SelectObject.name == "upColor1")
                {
                    SelectObject.GetComponent<CapsuleCollider>().isTrigger = false;
                    SelectObject.GetComponent<Rigidbody>().isKinematic = false;
                }

                else
                {
                    SelectObject.GetComponent<BoxCollider>().isTrigger = false;
                    SelectObject.GetComponent<Rigidbody>().isKinematic = false;
                }

                SelectObject.transform.position = lastTransform.position;
                SelectObject.transform.rotation = lastTransform.rotation;
                SelectObject.transform.localScale = lastTransform.localScale;
            }
        }

        if (menuAction.GetStateDown(handType))
        {
            if (MenuObject.activeSelf)
            {
                MenuObject.SetActive(false);
            }

            else
            {
                MenuObject.SetActive(true);
            }
        }

        if (grabGripAction.GetStateDown(handType))
        {

            if (SelectPrefab.activeSelf)
            {
                isPrefab = false;
                SelectObject.SetActive(true);
                SelectPrefab.SetActive(false);
            }

            else
            {
                isPrefab = true;
                SelectPrefab.SetActive(true);
                SelectObject.SetActive(false);

                SelectPrefab.transform.position = SelectObject.transform.position;
                SelectPrefab.transform.rotation = SelectObject.transform.rotation;
                SelectPrefab.transform.localScale = SelectObject.transform.localScale;
            }
        }

        if (isSize)
        {
            GameObject obj;
            if (isPrefab) obj = SelectPrefab;
            else obj = SelectObject;

            touchValue = teleportPos.GetAxis(handType);

            if (touchValue.y != 0)
            {
                if (!isSpeed)
                {
                    start = touchValue.y;
                    isSpeed = true;
                }
                end = touchValue.y;
                diff = end - start;
                start = touchValue.y;
            }
            else
            {
                start = end = 0.0f;
                diff = 0.0f;
                isSpeed = false;
            }
            size = diff * 0.1f;

            obj.transform.localScale += new Vector3(size, 0, size);
            if (isThick)
            {
                obj.transform.localScale += new Vector3(0, size, 0);
            }
        }

        if (grab.isGrab && isPrefab)
        {
            if (!isMoveStart)
            {
                if (!aa)
                {
                    lastTransform = SelectObject.transform;
                    aa = true;
                }
                StartCoroutine(SaveTransform());
                isMoveStart = true;
            }
        }

        else
        {
            isMoveStart = false;
        }
    }

    void SaveData(string filePath)
    {
        file = new FileStream(filePath, FileMode.Create, FileAccess.Write);
        writer = new StreamWriter(file, System.Text.Encoding.Unicode);

        for (int i = 0; i < moveDataList.Count; i++)
        {
            writer.WriteLine(moveDataList[i]);
        }

        writer.Close();
        file.Close();
    }

    void DecodeTransformData()
    {
        for (int i = 0; i < posList.Count; i++)
        {
            string transformData;

            transformData = "(" + posList[i].x + ", " + posList[i].y + ", " +
                posList[i].z + "), (" + rotList[i].x + ", " +
                rotList[i].y + ", " + rotList[i].z + "), (" +
                scaleList[i].x + ", " + scaleList[i].y + ", " + scaleList[i].z + ")";

            moveDataList.Add(transformData);
        }
    }

    void ShowLaser(RaycastHit hit)
    {
        laser.SetActive(true);
        laser.transform.position = Vector3.Lerp(controllerPose.transform.position, hitPoint, 0.5f);
        laserTransform.LookAt(hitPoint);
        laserTransform.localScale = new Vector3(laserTransform.localScale.x,
            laserTransform.localScale.y, hit.distance);
    }

    void saveBlack()
    {
        MenuObject.transform.GetChild(3).GetComponent<MeshRenderer>().material.color = Color.black;
    }

    void resetBlack()
    {
        MenuObject.transform.GetChild(4).GetComponent<MeshRenderer>().material.color = Color.black;
    }

    IEnumerator SaveTransform()
    {
        while (grab.isGrab)
        {
            posList.Add(SelectPrefab.transform.position);
            rotList.Add(SelectPrefab.transform.rotation.eulerAngles);
            scaleList.Add(SelectPrefab.transform.localScale);

            yield return new WaitForSeconds(0.001f);
        }
    }

    void ColorToBlue(GameObject obj)
    {
        for(int i=0;i<obj.transform.childCount;i++)
        {
            obj.transform.GetChild(i).GetComponent<MeshRenderer>().material.color = Color.blue;
        }
    }
}
